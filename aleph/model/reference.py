import logging

from sqlalchemy.orm import aliased

from aleph.core import db
from aleph.model.entity import Entity
from aleph.model.common import TimeStampedModel


log = logging.getLogger(__name__)


class Reference(db.Model, TimeStampedModel):
    id = db.Column(db.Integer(), primary_key=True)
    document_id = db.Column(db.BigInteger, db.ForeignKey('document.id'))
    entity_id = db.Column(db.Integer, db.ForeignKey('document.id'))
    selector_id = db.Column(db.Integer, db.ForeignKey('document.id'))
    weight = db.Column(db.Integer)

    entity_id = db.Column(db.Unicode(50), db.ForeignKey('entity.id'))
    entity = db.relationship(Entity, backref=db.backref('tags',
                                                        lazy='dynamic'))

    @classmethod
    def delete_set(cls, collection, package_id):
        q = db.session.query(cls)
        q = q.filter_by(collection=collection)
        q = q.filter_by(package_id=package_id)
        q.delete()

    @classmethod
    def by_package(cls, collection, package_id):
        etag = aliased(cls)
        ent = aliased(Entity)
        q = db.session.query(etag.entity_id, ent.name,
                             ent.category, ent.list_id)
        q = q.join(ent, ent.id == etag.entity_id)
        q = q.filter(etag.collection == collection)
        q = q.filter(etag.package_id == package_id)
        entities = []
        for entity_id, name, category, lst in q.all():
            entities.append({
                'id': entity_id,
                'entity': entity_id,
                'name': name,
                'category': category,
                'list': lst
            })
        return entities

    def __repr__(self):
        return '<EntityTag(%r, %r)>' % (self.package_id, self.entity_id)