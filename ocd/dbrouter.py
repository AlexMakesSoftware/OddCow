from django.apps import apps

class DbRouter(object):
    """
    A router to control all database operations on models
    """

    def db_for_read(self, model, **hints):
        """
        Attempts to read remote models go to remote database.
        """
        if getattr(model, 'my_meta_db_using', '') == 'legacy':
            return 'legacy'
        return 'default'

    def db_for_write(self, model, **hints):
        """
        Attempts to write remote models go to the remote database.
        """
        
        if getattr(model, 'my_meta_db_using', '') == 'legacy':
            return 'legacy'
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        # Don't have an opinion I guess. This means that it will only allow relations within databases.
        return None
    
    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Determine if the migration operation is allowed to run on the database with alias db.
        Return True if the operation should run, False if it shouldnt run, or None if the router has no opinion.
        """        

        if db == 'legacy' and app_label == 'farms':  
            print(f"Allowed {model_name} in {db} app:{app_label}")
            return True                  
        elif db == 'default' and app_label == 'farms':
            print(f"Rejected {model_name} in {db} app:{app_label}")
            return False
        else:
            if model_name:
                print(f"Allowed {model_name} in {db} app:{app_label}")
                return True
        
        print(f"Passed with no opinion on {model_name} in {db} app:{app_label}")
        return None
