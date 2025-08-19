import { verifyToken } from '../utils/auth';
import { openDatabase } from '../utils/db';

export default defineEventHandler(async (event) => {
    try {
        const userData = verifyToken(event.req);
        const db = await openDatabase();
        const todoList = await db.all('SELECT * FROM Todo where todo_list_id=(SELECT id FROM Todolist WHERE Todolist.user_id = ?)', [userData.userId]);

        const sharedList = await db.all('SELECT * FROM TodoShares where user_id= ? ', [userData.userId]);
        for (const shared of sharedList){
            if (shared.permission_type === "owner" || shared.permission_type === "shared")
            todoList.push(await db.get('SELECT * FROM Todo where id = ?',[shared.todo_id]));
        };
        return todoList;
    } catch (error) {
        return createError({
            statusCode: 401,
            statusMessage: 'Unauthorized: ' + error.message
        });
    }
});