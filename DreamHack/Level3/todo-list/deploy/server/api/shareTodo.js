import { readBody, createError } from 'h3';
import { openDatabase } from '../utils/db';

export default defineEventHandler(async (event) => {
    const userData = verifyToken(event.req);
    const db = await openDatabase();
    const body = await readBody(event);
    
    const todo = body;
    try {
        const todo_data = await db.get(
            'SELECT * FROM Todo WHERE id = ?', [todo.id]
        );
        if (todo_data.is_completed === 1) {
            return { message: 'you cannot share already completed todo', id: todo_data.id}
        }

        const result = await db.run(
            `INSERT INTO TodoShares (todo_id, user_id, permission_type) VALUES
            (?, ?, ?)`,
            [todo_data.id, todo.target_id, 'shared']
          );
        return { success: true, message: 'Todo shared successfully', id: result.lastID };
    } catch (error) {
        throw createError({ statusCode: 500, statusMessage: 'Database error: ' + error.message });
    }
});