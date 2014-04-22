# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Survey.pub_date'
        db.alter_column('assessment_survey', 'pub_date', self.gf('django.db.models.fields.DateTimeField')())
        # Adding field 'Result.score_percentage'
        db.add_column('assessment_result', 'score_percentage',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=0, max_length=3),
                      keep_default=False)


    def backwards(self, orm):

        # Changing field 'Survey.pub_date'
        db.alter_column('assessment_survey', 'pub_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True))
        # Deleting field 'Result.score_percentage'
        db.delete_column('assessment_result', 'score_percentage')


    models = {
        'assessment.answer': {
            'Meta': {'unique_together': "(('result', 'question'),)", 'object_name': 'Answer'},
            'answer': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['assessment.Question']", 'related_name': "'answers'"}),
            'result': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['assessment.Result']", 'related_name': "'answers'"})
        },
        'assessment.choice': {
            'Meta': {'ordering': "['id']", 'object_name': 'Choice'},
            'choice_value': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_correct': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['assessment.Question']"})
        },
        'assessment.question': {
            'Meta': {'ordering': "['survey', 'id']", 'object_name': 'Question'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'of_type': ('django.db.models.fields.IntegerField', [], {'default': '1', 'max_length': '1'}),
            'question': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'survey': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['assessment.Survey']"})
        },
        'assessment.result': {
            'Meta': {'unique_together': "(('survey', 'user'),)", 'object_name': 'Result'},
            'completed_on': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True', 'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'score': ('django.db.models.fields.CharField', [], {'default': '0', 'max_length': '10'}),
            'score_percentage': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'max_length': '3'}),
            'survey': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['assessment.Survey']", 'related_name': "'results'"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'related_name': "'results'"})
        },
        'assessment.survey': {
            'Meta': {'ordering': "['pub_date']", 'object_name': 'Survey'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'due_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255', 'unique': 'True'})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'unique': 'True'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)", 'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'related_name': "'user_set'", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'related_name': "'user_set'", 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '30', 'unique': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'ordering': "('name',)", 'db_table': "'django_content_type'", 'object_name': 'ContentType'},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['assessment']