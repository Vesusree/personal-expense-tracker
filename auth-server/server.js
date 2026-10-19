
require("dotenv").config();

const express = require("express");
const fs = require("fs");
const path = require("path");
const crypto = require("crypto");
const mysql = require("mysql2/promise");
const nodemailer = require("nodemailer");
const bcrypt = require("bcryptjs");
const jwt = require("jsonwebtoken");

const app = express();
app.use(express.json());

const pool = mysql.createPool({
  host: process.env.DB_HOST,
  port: Number(process.env.DB_PORT),
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
  database: process.env.DB_NAME,
  ssl: {
    ca: fs.readFileSync(path.join(__dirname, "ca.pem")),
    rejectUnauthorized: true
  },
  waitForConnections: true,
  connectionLimit: 5
});

const transporter = nodemailer.createTransport({
  service: "gmail",
  auth: {
    user: process.env.EMAIL_USER,
    pass: process.env.EMAIL_APP_PASSWORD
  }
});

function createVerificationToken() {
  return crypto.randomBytes(32).toString("hex");
}

function hashToken(token) {
  return crypto.createHash("sha256").update(token).digest("hex");
}

function createJwt(user) {
  return jwt.sign(
    { id: user.id, email: user.email },
    process.env.JWT_SECRET,
    { expiresIn: "2h" }
  );
}

function authenticateToken(req, res, next) {
  const authHeader = req.headers.authorization;
  const token = authHeader && authHeader.startsWith("Bearer ")
    ? authHeader.slice(7)
    : null;

  if (!token) {
    return res.status(401).json({ message: "Authentication token required." });
  }

  try {
    req.user = jwt.verify(token, process.env.JWT_SECRET);
    next();
  } catch {
    return res.status(401).json({ message: "Invalid or expired token." });
  }
}

app.get("/", (req, res) => {
  res.json({ message: "Expense Tracker authentication API is running." });
});

app.post("/register", async (req, res) => {
  try {
    const { name, email, password } = req.body;

    if (
      typeof name !== "string" ||
      typeof email !== "string" ||
      typeof password !== "string" ||
      !name.trim() ||
      !email.trim() ||
      password.length < 8
    ) {
      return res.status(400).json({
        message: "Enter your name, a valid email, and a password of at least 8 characters."
      });
    }

    const normalizedEmail = email.trim().toLowerCase();

    const [existing] = await pool.execute(
      "SELECT id FROM users WHERE email = ?",
      [normalizedEmail]
    );

    if (existing.length > 0) {
      return res.status(409).json({
        message: "An account with this email already exists."
      });
    }

    const passwordHash = await bcrypt.hash(password, 12);
    const token = createVerificationToken();
    const tokenHash = hashToken(token);

    const [result] = await pool.execute(
      `INSERT INTO users
       (name, email, password_hash, is_verified,
        verification_token_hash, verification_expires_at)
       VALUES (?, ?, ?, FALSE, ?, DATE_ADD(UTC_TIMESTAMP(), INTERVAL 30 MINUTE))`,
      [name.trim(), normalizedEmail, passwordHash, tokenHash]
    );

    const verificationUrl =
      `${process.env.APP_BASE_URL}/verify-email?token=${token}&email=${encodeURIComponent(normalizedEmail)}`;

    try {
      await transporter.sendMail({
        from: process.env.EMAIL_USER,
        to: normalizedEmail,
        subject: "Verify your Expense Tracker account",
        text: `Hello ${name.trim()},\n\nVerify your email using this link (valid for 30 minutes):\n${verificationUrl}\n\nIf you did not register, you can ignore this email.`
      });
    } catch (mailError) {
      await pool.execute("DELETE FROM users WHERE id = ?", [result.insertId]);
      console.error("Verification email failed:", mailError.message);
      return res.status(502).json({
        message: "The verification email could not be sent. Check the email configuration and try again."
      });
    }

    return res.status(201).json({
      message: "Registration successful. Check your email to verify your account."
    });
  } catch (error) {
    console.error("Registration error:", error.message);
    return res.status(500).json({ message: "Registration failed." });
  }
});

app.get("/verify-email", async (req, res) => {
  try {
    const { token, email } = req.query;

    if (typeof token !== "string" || typeof email !== "string") {
      return res.status(400).send("Invalid verification link.");
    }

    const [result] = await pool.execute(
      `UPDATE users
       SET is_verified = TRUE,
           verification_token_hash = NULL,
           verification_expires_at = NULL
       WHERE email = ?
         AND verification_token_hash = ?
         AND verification_expires_at > UTC_TIMESTAMP()
         AND is_verified = FALSE`,
      [email.trim().toLowerCase(), hashToken(token)]
    );

    if (result.affectedRows !== 1) {
      return res.status(400).send("This verification link is invalid or expired.");
    }

    return res.send("Email verified successfully. You can now log in.");
  } catch (error) {
    console.error("Verification error:", error.message);
    return res.status(500).send("Email verification failed.");
  }
});

app.post("/login", async (req, res) => {
  try {
    const { email, password } = req.body;

    if (typeof email !== "string" || typeof password !== "string") {
      return res.status(400).json({ message: "Enter your email and password." });
    }

    const [rows] = await pool.execute(
      "SELECT id, name, email, password_hash, is_verified FROM users WHERE email = ?",
      [email.trim().toLowerCase()]
    );

    if (rows.length === 0) {
      return res.status(401).json({ message: "Invalid email or password." });
    }

    const user = rows[0];
    const passwordMatches = await bcrypt.compare(password, user.password_hash);

    if (!passwordMatches) {
      return res.status(401).json({ message: "Invalid email or password." });
    }

    if (!user.is_verified) {
      return res.status(403).json({ message: "Please verify your email before logging in." });
    }

    const token = createJwt(user);

    return res.json({
      message: "Login successful.",
      token,
      user: { id: user.id, name: user.name, email: user.email }
    });
  } catch (error) {
    console.error("Login error:", error.message);
    return res.status(500).json({ message: "Login failed." });
  }
});

app.get("/me", authenticateToken, async (req, res) => {
  try {
    const [rows] = await pool.execute(
      "SELECT id, name, email FROM users WHERE id = ?",
      [req.user.id]
    );

    if (rows.length === 0) {
      return res.status(404).json({ message: "User not found." });
    }

    return res.json({ user: rows[0] });
  } catch (error) {
    console.error("Profile error:", error.message);
    return res.status(500).json({ message: "Could not load profile." });
  }
});

const port = Number(process.env.PORT) || 3000;

async function startServer() {
  if (!process.env.JWT_SECRET || process.env.JWT_SECRET.length < 32) {
    throw new Error("JWT_SECRET must be at least 32 characters long.");
  }

  await pool.query("SELECT 1");
  await transporter.verify();

  app.listen(port, () => {
    console.log(`Authentication API running on port ${port}`);
    console.log("MySQL and email connections verified.");
  });
}

startServer().catch(async (error) => {
  console.error("Could not start authentication API:", error.message);
  await pool.end();
  process.exit(1);
});
