class AccountsRouter:
    """
    A router to control all database operations
    on models of accounts data.
    """
    route_app_labels = {
        'auth', 'contenttypes', 'admin', 'sessions'
    }

    def db_for_read(self, model, **hints):
        if model._meta.app_label in self.route_app_labels:
            return 'accounts_db'

    def db_for_write(self, model, **hints):
        if model._meta.app_label in self.route_app_labels:
            return 'accounts_db'

    def allow_relation(self, obj1, obj2, **hints):
        if (obj1._meta.app_label in self.route_app_labels or
                obj2._meta.app_label in self.route_app_labels):
            return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label in self.route_app_labels:
            return db == 'accounts_db'
