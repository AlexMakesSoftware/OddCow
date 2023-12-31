from django.apps import apps
import sys

class DbRouter(object):
    """
    A router to control all database operations on models
    """

    def db_for_read(self, model, **hints):
        """
        Attempts to read remote models go to remote database.
        """
        if 'test' in sys.argv:  # Check if running tests
            return 'default'  # Use the test database for legacy models during testing
        
        if getattr(model, 'my_meta_db_using', '') == 'legacy':
            return 'legacy'
        return 'default'

    def db_for_write(self, model, **hints):
        """
        Attempts to write remote models go to the remote database.
        """
        if 'test' in sys.argv:  # Check if running tests
            return 'default'  # Use the test database for legacy models during testing
        
        if getattr(model, 'my_meta_db_using', '') == 'legacy':
            return 'legacy'
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.app_label == obj2._meta.app_label:
            return True
        return None
    
    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Determine if the migration operation is allowed to run on the database with alias db.
        Return True if the operation should run, False if it shouldnt run, or None if the router has no opinion.
        """        

        if db == 'legacy' and app_label == 'farms':              
            return True                  
        elif db == 'default' and app_label == 'farms':            
            return False
        else:
            if model_name:                
                return True
        
        # TODO: make sure that the admin stuff and the default tables don't ever go into the legacy db.        
        return None
