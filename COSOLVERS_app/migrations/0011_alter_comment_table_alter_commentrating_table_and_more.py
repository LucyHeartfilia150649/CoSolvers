from django.db import migrations


def rename_tables_if_needed(apps, schema_editor):
    statements = [
        (
            "COSOLVERS_app_comment",
            "viable_graph_app_comment",
        ),
        (
            "COSOLVERS_app_commentrating",
            "viable_graph_app_commentrating",
        ),
        (
            "COSOLVERS_app_problem",
            "viable_graph_app_problem",
        ),
        (
            "COSOLVERS_app_suggestion",
            "viable_graph_app_suggestion",
        ),
        (
            "COSOLVERS_app_userprofile",
            "viable_graph_app_userprofile",
        ),
    ]

    with schema_editor.connection.cursor() as cursor:
        for old_table, new_table in statements:
            cursor.execute(
                """
                SELECT EXISTS (
                    SELECT 1
                    FROM information_schema.tables
                    WHERE table_schema = 'public'
                      AND table_name = %s
                )
                """,
                [new_table],
            )
            target_exists = cursor.fetchone()[0]

            cursor.execute(
                """
                SELECT EXISTS (
                    SELECT 1
                    FROM information_schema.tables
                    WHERE table_schema = 'public'
                      AND table_name = %s
                )
                """,
                [old_table],
            )
            source_exists = cursor.fetchone()[0]

            if not target_exists and source_exists:
                cursor.execute(f'ALTER TABLE "{old_table}" RENAME TO "{new_table}"')


class Migration(migrations.Migration):

    dependencies = [
        ("COSOLVERS_app", "0010_alter_problem_reported_by"),
    ]

    operations = [
        migrations.RunPython(
            rename_tables_if_needed,
            reverse_code=migrations.RunPython.noop,
        ),
        migrations.SeparateDatabaseAndState(
            database_operations=[],
            state_operations=[
                migrations.AlterModelTable(
                    name="comment",
                    table="viable_graph_app_comment",
                ),
                migrations.AlterModelTable(
                    name="commentrating",
                    table="viable_graph_app_commentrating",
                ),
                migrations.AlterModelTable(
                    name="problem",
                    table="viable_graph_app_problem",
                ),
                migrations.AlterModelTable(
                    name="suggestion",
                    table="viable_graph_app_suggestion",
                ),
                migrations.AlterModelTable(
                    name="userprofile",
                    table="viable_graph_app_userprofile",
                ),
            ],
        ),
    ]
