import { readBody, createError } from 'h3';
import bcrypt from 'bcryptjs';
import { openDatabase } from '../utils/db';



export default async (req, res) => {
    const db = await openDatabase();
    const { username, email, password } = await readBody(req);

    if (!username || !email || !password) {
        throw createError({ statusCode: 400, statusMessage: 'All fields are required.' });
    }

    const hashedPassword = await bcrypt.hash(password, 10);

    try {
        await db.run('BEGIN');  
        const result = await db.run('INSERT INTO Users (username, email, password) VALUES (?, ?, ?)', [username, email, hashedPassword]);
        await db.run('INSERT INTO Todolist (user_id, name) VALUES (?, ?)', [result.lastID, 'Default List']);
        await db.run('COMMIT'); 
        return { message: 'User registered successfully.', userId: result.lastID };
    } catch (error) {
        await db.run('ROLLBACK'); 
        if (error.code === 'SQLITE_CONSTRAINT') {
            throw createError({ statusCode: 409, statusMessage: 'Username or email already exists.' });
        } else {
            throw createError({ statusCode: 500, statusMessage: 'Could not register user.' });
        }
    }
}