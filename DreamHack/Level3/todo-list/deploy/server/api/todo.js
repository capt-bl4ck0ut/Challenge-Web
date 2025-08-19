import { readBody, createError } from 'h3';
import { openDatabase } from '../utils/db';

export default defineEventHandler(async (event) => {
    const userData = verifyToken(event.req);
    const db = await openDatabase();
    const body = await readBody(event);
    
    const { title, description, dueDate } = body;
    if (!title || !description) {
        throw createError({ statusCode: 400, statusMessage: 'Title and description are required.' });
    }

    const startDate = new Date().toISOString();
    const dueDateFormatted = dueDate ? new Date(dueDate).toISOString() : null;

    try {
        const todoListId = await db.get('SELECT id FROM Todolist WHERE user_id = ?', [userData.userId]);
        const result = await db.run(
            `INSERT INTO todo (todo_list_id, title, description, start_date, due_date)
             VALUES (?, ?, ?, ?, ?)`,
            [todoListId.id, title, description, startDate, dueDateFormatted]
        );
        return { success: true, message: 'Todo added successfully', id: result.lastID };
    } catch (error) {
        throw createError({ statusCode: 500, statusMessage: 'Database error: ' + error.message });
    }
});