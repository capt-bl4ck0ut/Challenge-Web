import { createError, readBody } from 'h3';
import bcrypt from 'bcryptjs';
import { openDatabase } from '../utils/db';
import jwt from 'jsonwebtoken';

const JWT_SECRET_KEY = process.env.JWT_SECRET_KEY || 'your_secret_key';
export default async (req, res) => {
    const db = await openDatabase();
    const { email, password } = await readBody(req);

    if (!email || !password) {
        throw createError({ statusCode: 400, statusMessage: 'Email and password are required.' });
    }

    try {
        const user = await db.get('SELECT * FROM Users WHERE email = ?', [email]);
        if (!user) {
            throw createError({ statusCode: 404, statusMessage: 'User not found!' });
        }

        const passwordValid = await bcrypt.compare(password, user.password);
        if (!passwordValid) {
            throw createError({ statusCode: 401, statusMessage: 'Invalid password!' });
        }

        const token = jwt.sign(
            { userId: user.id, email: user.email }, 
            JWT_SECRET_KEY,
            { expiresIn: '3h' } 
        );

        return { message: 'Login successful!', token }; 
    } catch (error) {
        throw createError({ statusCode: 500, statusMessage: 'Error logging in user.' });
    }
}
