from django.db import migrations


def repair_userprofile_user_fk(apps, schema_editor):
    """Ensure existing PostgreSQL schemas cascade UserProfile when User is deleted."""
    if schema_editor.connection.vendor != "postgresql":
        return

    with schema_editor.connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT child.relname, constraint_name
            FROM pg_constraint constraint_data
            JOIN pg_class child ON child.oid = constraint_data.conrelid
            JOIN pg_class parent ON parent.oid = constraint_data.confrelid
            CROSS JOIN LATERAL (
                SELECT constraint_data.conname AS constraint_name
            ) constraint_info
            WHERE constraint_data.contype = 'f'
              AND child.relname LIKE '%userprofile'
              AND parent.relname = 'auth_user'
              AND constraint_data.conkey = ARRAY[
                  (
                      SELECT attnum
                      FROM pg_attribute
                      WHERE attrelid = constraint_data.conrelid
                        AND attname = 'user_id'
                  )::smallint
              ]
            """
        )
        constraints = cursor.fetchall()

        for table_name, constraint_name in constraints:
            quoted_table = schema_editor.quote_name(table_name)
            quoted_constraint = schema_editor.quote_name(constraint_name)
            cursor.execute(
                f"ALTER TABLE {quoted_table} DROP CONSTRAINT {quoted_constraint}"
            )
            cursor.execute(
                f"ALTER TABLE {quoted_table} "
                f"ADD CONSTRAINT {quoted_constraint} "
                "FOREIGN KEY (user_id) REFERENCES auth_user(id) ON DELETE CASCADE"
            )


class Migration(migrations.Migration):
    dependencies = [
        ("COSOLVERS_app", "0007_problem_is_approved"),
    ]

    operations = [
        migrations.RunPython(
            repair_userprofile_user_fk,
            migrations.RunPython.noop,
        ),
    ]