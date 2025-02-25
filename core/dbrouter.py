class ProdMonDBRouter(object):
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'panda':
            return 'default'
        if model._meta.app_label == 'pandaarch':
            return 'panda_atlarc'
        if model._meta.app_label == 'pandamon':
            return 'default'
        if model._meta.app_label == 'harvester':
            return 'default'
        if model._meta.app_label == 'idds':
            return 'idds'
        if model._meta.app_label == 'jedi':
            return 'default'
        if model._meta.app_label == "taskmon":
            return "default"
        return None

    def db_for_write(self, model, **hints):
        return None

    def allow_relation(self, obj1, obj2, **hints):
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        return None
