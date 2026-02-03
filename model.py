from common import format_mark

class Config:
    def __init__(self, title):
        self.title = title
        self.ignore_regionals = False
        self.events = dict()
        self.quotas = {}

    def add_event(self, event_title, event_ids):
        for event_id in event_ids.split(','):
            self.events[event_id] = event_title

class Event:
    def __init__(self, id, label, title):
        self.id = id
        self.label = label
        self.title = title
        self.categories = dict()

    def add_category(self, category):
        self.categories[category.label] = category

    def get_category_names(self):
        return list(self.categories.keys())

    def get_category(self, category_name):
        return self.categories[category_name]

    def to_string(self):
        s = f'---Event\nId: {self.id}, Label: {self.label}, Title: {self.title}, Categories:\n'
        #for category in self.categories.keys():
            #s += f'{self.categories[category].to_string()}\n'
        return s

class Category:
    def __init__(self, label):
        self.label = label
        self.general_ranking = []
        self.apparatus_rankings = dict()

    def add_apparatus_ranking(self, apparatus_label, apparatus_ranking):
        self.apparatus_rankings[apparatus_label] = apparatus_ranking

    def add_entity_apparatus_to_apparatus_ranking(self, apparatus, entity):
        if apparatus not in self.apparatus_rankings.keys():
            self.apparatus_rankings[apparatus] = []
        self.apparatus_rankings[apparatus].append(entity)

    def sort_apparatus_rankings(self):
        for apparatus in self.apparatus_rankings.keys():
            self.apparatus_rankings[apparatus].sort(key=lambda e: float(e.apparatuses[apparatus].total), reverse=True)

    def is_empty(self):
        return len(self.general_ranking[0]) == 0

    def get_apparatus_names(self):
        return list(self.general_ranking[0][0].apparatuses.keys())

    def to_string(self):
        s = f'---Category\nLabel: {self.label}, General ranking:\n'
        for rank in self.general_ranking:
            for entity in rank:
                s += f'{entity.to_string()}\n'
        for apparatus in self.apparatus_rankings.keys():
            s += f'Appartus ranking ({apparatus})\n'
            for entity in self.apparatus_rankings[apparatus]:
                s += f'{entity.to_string()}\n'
        return s

class Entity:
    def __init__(self, name, event_title, club, initial_rank, total):
        self.name = name
        self.event_title = event_title
        self.event_label = ""
        self.club = club
        self.initial_rank = initial_rank
        self.rank = 0
        self.total = total
        self.apparatuses = dict()

    def add_apparatus(self, apparatus_name, apparatus):
        self.apparatuses[apparatus_name] = apparatus

    def get_apparatus_names(self):
        return self.apparatuses.keys()

    def get_apparatuses_number(self):
        return len(self.get_apparatus_names())

    def to_string(self):
        s = f'---Entity\nName: {self.name}, event: {self.event_title}, Club: {self.club}, Initial rank: {self.initial_rank}, Total: {self.total}, Apparatuses:'
        for apparatus in self.apparatuses.keys():
            s += f'\n{apparatus}: {self.apparatuses[apparatus].to_string()}'
        return s

class Apparatus:
    MARK_TYPES = ['DB', 'DA', 'Art.', 'Exé.', 'Pén.']

    def __init__(self):
        self.total = 0
        self.db = 0
        self.da = 0
        self.artistry = 0
        self.execution = 0
        self.penalty = 0

    def set_corps_mark(self, corps, mark):
        if corps in self.MARK_TYPES:
            mark_float = format_mark(mark)
            if corps == 'DB':
                self.db = mark_float
            elif corps == 'DA':
                self.da = mark_float
            elif corps == 'Art.':
                self.artistry = mark_float
            elif corps == 'Exé.':
                self.execution = mark_float
            elif corps == 'Pén.':
                self.penalty = mark_float

    def to_string(self):
        return f'---Apparatus\nTotal: {self.total}, DB: {self.db}, DA: {self.da}, A: {self.artistry}, E: {self.execution}, P: {self.penalty}'

class Club:
    def __init__(self):
        self.nat = []
        self.fed = []

    def get_result(self):
        nationales = sorted(self.nat, reverse=True)
        federales = sorted(self.fed, reverse=True)
        if not nationales or not federales or len(federales) < 3:
            return {"gymnasts": [], "total": 0}
        gymnasts = [nationales[0], federales[0], federales[1], federales[2]]
        return {"gymnasts": gymnasts, "total": sum(mark for mark,_ in gymnasts)}

    def add_mark(self, gymnast_name, division, mark):
        if division == 'fed':
            self.fed.append((mark, gymnast_name))
        elif division == 'nat':
            self.nat.append((mark, gymnast_name))
