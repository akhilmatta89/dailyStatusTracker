import sqlite3
import db_operations.constants

from flask import jsonify


class UpdateData:

    def update_status_based_on_date(self, date, data):
        # Identify which keys the user has sent
        global conn
        sent_keys = list(data.keys())

        # Generate SQL SET clause dynamically based on provided fields
        update_fields = []
        values = []

        for key, value in data.items():
            update_fields.append(f"{key} = ?")
            values.append(value)

        if not update_fields:
            return jsonify({"error": "No valid fields to update"}), 400

        # Prepare the UPDATE query
        update_query = f"UPDATE daily_status SET {', '.join(update_fields)} WHERE Date = ?"
        values.append(date)  # Add date as the WHERE condition
        try:
            conn = sqlite3.connect(db_operations.constants.DB_PATH)

            cursor = conn.cursor()
            cursor.execute(update_query, values)
            conn.commit()

            # Check if any row was updated
            if cursor.rowcount == 0:
                return jsonify({"error": "No task found for the specified date"}), 404

            return jsonify({"message": "Task updated successfully", "updated_fields": sent_keys}), 200

        except sqlite3.Error as e:
            return jsonify({"error": f"An error occurred: {str(e)}"}), 500

        finally:
            conn.close()