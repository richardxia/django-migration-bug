# Bug in Django migrations when using `order_with_respect_to`

This project demonstrates a bug with the way Django generates migrations when a
model has the `order_with_respect_to` option set along with a `unique_together`
which includes the implicit `_order` field created by the
`order_with_respect_to`.

When you run `./manage.py makemigrations`, it creates a migration file that
fails to apply cleanly, leading to the following stacktrace:


```pytb
$ ./manage.py migrate
Operations to perform:
  Apply all migrations: admin, contenttypes, myapp, auth, sessions
Running migrations:
  Rendering model states... DONE
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying admin.0001_initial... OK
  Applying admin.0002_logentry_remove_auto_add... OK
  Applying contenttypes.0002_remove_content_type_name... OK
  Applying auth.0002_alter_permission_name_max_length... OK
  Applying auth.0003_alter_user_email_max_length... OK
  Applying auth.0004_alter_user_username_opts... OK
  Applying auth.0005_alter_user_last_login_null... OK
  Applying auth.0006_require_contenttypes_0002... OK
  Applying auth.0007_alter_validators_add_error_messages... OK
  Applying myapp.0001_initial...Traceback (most recent call last):
  File "./manage.py", line 10, in <module>
    execute_from_command_line(sys.argv)
  File "/Users/rxia/envs/tmp/lib/python2.7/site-packages/django/core/management/__init__.py", line 353, in execute_from_command_line
    utility.execute()
  File "/Users/rxia/envs/tmp/lib/python2.7/site-packages/django/core/management/__init__.py", line 345, in execute
    self.fetch_command(subcommand).run_from_argv(self.argv)
  File "/Users/rxia/envs/tmp/lib/python2.7/site-packages/django/core/management/base.py", line 348, in run_from_argv
    self.execute(*args, **cmd_options)
  File "/Users/rxia/envs/tmp/lib/python2.7/site-packages/django/core/management/base.py", line 399, in execute
    output = self.handle(*args, **options)
  File "/Users/rxia/envs/tmp/lib/python2.7/site-packages/django/core/management/commands/migrate.py", line 200, in handle
    executor.migrate(targets, plan, fake=fake, fake_initial=fake_initial)
  File "/Users/rxia/envs/tmp/lib/python2.7/site-packages/django/db/migrations/executor.py", line 92, in migrate
    self._migrate_all_forwards(plan, full_plan, fake=fake, fake_initial=fake_initial)
  File "/Users/rxia/envs/tmp/lib/python2.7/site-packages/django/db/migrations/executor.py", line 121, in _migrate_all_forwards
    state = self.apply_migration(state, migration, fake=fake, fake_initial=fake_initial)
  File "/Users/rxia/envs/tmp/lib/python2.7/site-packages/django/db/migrations/executor.py", line 198, in apply_migration
    state = migration.apply(state, schema_editor)
  File "/Users/rxia/envs/tmp/lib/python2.7/site-packages/django/db/migrations/migration.py", line 123, in apply
    operation.database_forwards(self.app_label, schema_editor, old_state, project_state)
  File "/Users/rxia/envs/tmp/lib/python2.7/site-packages/django/db/migrations/operations/models.py", line 359, in database_forwards
    getattr(new_model._meta, self.option_name, set()),
  File "/Users/rxia/envs/tmp/lib/python2.7/site-packages/django/db/backends/sqlite3/schema.py", line 261, in alter_unique_together
    self._remake_table(model, override_uniques=new_unique_together)
  File "/Users/rxia/envs/tmp/lib/python2.7/site-packages/django/db/backends/sqlite3/schema.py", line 181, in _remake_table
    self.create_model(temp_model)
  File "/Users/rxia/envs/tmp/lib/python2.7/site-packages/django/db/backends/base/schema.py", line 272, in create_model
    columns = [model._meta.get_field(field).column for field in fields]
  File "/Users/rxia/envs/tmp/lib/python2.7/site-packages/django/db/models/options.py", line 582, in get_field
    raise FieldDoesNotExist('%s has no field named %r' % (self.object_name, field_name))
django.core.exceptions.FieldDoesNotExist: Foo has no field named u'_order'
```

This occurs because the order of operations in the migration is incorrect. It
first attempts to set the `unique_together` *before* it actually creates the
`_order` field.
