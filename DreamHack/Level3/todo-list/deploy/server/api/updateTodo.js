import { readBody, createError } from 'h3';
import { openDatabase } from '../utils/db';

export default defineEventHandler(async (event) => {
    const userData = verifyToken(event.req);
    const db = await openDatabase();
    const body = await readBody(event);
    
    const { id, value} = body;
    try {
        const result = await db.run(
            `UPDATE todo
             SET is_completed = ?
             WHERE id = ?`,
            [value, id]
          );
        return { success: true, message: 'Todo updated successfully', id: result.lastID };
    } catch (error) {
        throw createError({ statusCode: 500, statusMessage: 'Database error: ' + error.message });
    }
});