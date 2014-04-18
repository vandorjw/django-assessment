# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Survey'
        db.create_table('assessment_survey', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('pub_date', self.gf('django.db.models.fields.DateTimeField')(blank=True, default=datetime.datetime.now, auto_now=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('assessment', ['Survey'])

        # Adding model 'Question'
        db.create_table('assessment_question', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('survey', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['assessment.Survey'])),
            ('question', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('of_type', self.gf('django.db.models.fields.IntegerField')(max_length=1, default=1)),
        ))
        db.send_create_signal('assessment', ['Question'])

        # Adding model 'Choice'
        db.create_table('assessment_choice', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['assessment.Question'])),
            ('choice_value', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('is_correct', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('assessment', ['Choice'])

        # Adding model 'Result'
        db.create_table('assessment_result', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('survey', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['assessment.Survey'], related_name='results')),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], related_name='results')),
            ('completed_on', self.gf('django.db.models.fields.DateTimeField')(blank=True, default=datetime.datetime.now, auto_now=True)),
            ('score', self.gf('django.db.models.fields.CharField')(max_length=10, default=0)),
        ))
        db.send_create_signal('assessment', ['Result'])

        # Adding unique constraint on 'Result', fields ['survey', 'user']
        db.create_unique('assessment_result', ['survey_id', 'user_id'])

        # Adding model 'Answer'
        db.create_table('assessment_answer', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('result', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['assessment.Result'], related_name='answers')),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['assessment.Question'], related_name='answers')),
            ('answer', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('assessment', ['Answer'])

        # Adding unique constraint on 'Answer', fields ['result', 'question']
        db.create_unique('assessment_answer', ['result_id', 'question_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'Answer', fields ['result', 'question']
        db.delete_unique('assessment_answer', ['result_id', 'question_id'])

        # Removing unique constraint on 'Result', fields ['survey', 'user']
        db.delete_unique('assessment_result', ['survey_id', 'user_id'])

        # Deleting model 'Survey'
        db.delete_table('assessment_survey')

        # Deleting model 'Question'
        db.delete_table('assessment_question')

        # Deleting model 'Choice'
        db.delete_table('assessment_choice')

        # Deleting model 'Result'
        db.delete_table('assessment_result')

        # Deleting model 'Answer'
        db.delete_table('assessment_answer')


    models = {
        'assessment.answer': {
            'Meta': {'object_name': 'Answer', 'unique_together': "(('result', 'question'),)"},
            'answer': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['assessment.Question']", 'related_name': "'answers'"}),
            'result': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['assessment.Result']", 'related_name': "'answers'"})
        },
        'assessment.choice': {
            'Meta': {'object_name': 'Choice', 'ordering': "['id']"},
            'choice_value': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_correct': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['assessment.Question']"})
        },
        'assessment.question': {
            'Meta': {'object_name': 'Question', 'ordering': "['survey', 'id']"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'of_type': ('django.db.models.fields.IntegerField', [], {'max_length': '1', 'default': '1'}),
            'question': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'survey': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['assessment.Survey']"})
        },
        'assessment.result': {
            'Meta': {'object_name': 'Result', 'unique_together': "(('survey', 'user'),)"},
            'completed_on': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'default': 'datetime.datetime.now', 'auto_now': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'score': ('django.db.models.fields.CharField', [], {'max_length': '10', 'default': '0'}),
            'survey': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['assessment.Survey']", 'related_name': "'results'"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'related_name': "'results'"})
        },
        'assessment.survey': {
            'Meta': {'object_name': 'Survey', 'ordering': "['pub_date']"},
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'default': 'datetime.datetime.now', 'auto_now': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255'})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'to': "orm['auth.Permission']", 'symmetrical': 'False'})
        },
        'auth.permission': {
            'Meta': {'object_name': 'Permission', 'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)"},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'blank': 'True', 'max_length': '75'}),
            'first_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'to': "orm['auth.Group']", 'symmetrical': 'False', 'related_name': "'user_set'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'to': "orm['auth.Permission']", 'symmetrical': 'False', 'related_name': "'user_set'"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'db_table': "'django_content_type'", 'object_name': 'ContentType', 'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['assessment']