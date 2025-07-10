# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError


class IsMailingListAssistant(models.Model):
    _name = 'is.mailing.list.assistant'
    _description = "Assistant de création de mailing list"
    _order = 'name'

    name    = fields.Char("Nom", required=True, index=True)
    list_id = fields.Many2one('mailing.list', "Liste de diffusion")
    mails   = fields.Text("Mails",help="Liste des mails (un mail par ligne) à traiter par cet assistant")


    def desactiver_contacts(self):
        for obj in self:
            mails = obj.mails.split("\n")
            for mail in mails:
                mail = mail.strip()
                contacts = self.env['mailing.contact'].search([('email','=',mail)])
                for contact in contacts:
                    contact.active=False


    def ajouter_contacts(self):
        for obj in self:
            list_id = obj.list_id.id
            if list_id:
                mails = obj.mails.split('\n')
                for line in mails:
                    mail = line.strip()
                    if mail!='':
                        contacts = self.env['mailing.contact'].search([('email','=',mail)])
                        for contact in contacts:
                            ids=[]
                            for line in contact.subscription_list_ids:
                                ids.append(line.list_id.id)
                            if list_id not in ids:
                                vals={
                                    'list_id'   : list_id,
                                    'contact_id': contact.id,
                                }
                                res = self.env['mailing.contact.subscription'].create(vals)


class IsSegment(models.Model):
    _name = 'is.segment'
    _description = "Segment"
    _order = 'name'

    name = fields.Char("Segment", required=True, index=True)


class IsRegion(models.Model):
    _name = 'is.region'
    _description = "Région"
    _order = 'name'

    name = fields.Char("Région", required=True, index=True)


class MassMailingContact(models.Model):
    _inherit = 'mailing.contact'

    is_code_ape      = fields.Char(string='Code APE')
    is_ville         = fields.Char(string='Ville')
    is_code_postal   = fields.Char(string='Code Postal')
    is_rue           = fields.Char(string='Rue')
    is_region_id     = fields.Many2one('is.region', "Région")
    is_telephone     = fields.Char(string='Numéro de téléphone')
    is_fax           = fields.Char(string='Numéro de fax')
    is_site_internet = fields.Char(string='Site internet')
    is_segment_id    = fields.Many2one('is.segment', "Segment")
    active           = fields.Boolean(string='Actif',default=True)


    def add_last_mailing_list_action(self):
        lists = self.env['mailing.list'].search([], limit=1, order='id desc')
        if len(lists):
            for obj in self.browse(self.env.context['active_ids']):
                list_id = lists[0].id
                ids=[]
                for line in obj.subscription_list_ids:
                    ids.append(line.list_id.id)
                if list_id not in ids:
                    vals={
                        'list_id'   : list_id,
                        'contact_id': obj.id,
                    }
                    res = self.env['mailing.contact.subscription'].create(vals)


