export const queryKeys = {
  learners: {
    all: ['learners'],
    list: (params) => ['learners', 'list', params],
    detail: (id) => ['learners', 'detail', id],
  },
  persons: {
    all: ['persons'],
    detail: (id) => ['persons', 'detail', id],
  },
  programs: {
    all: ['programs'],
    list: (params) => ['programs', 'list', params],
    detail: (id) => ['programs', 'detail', id],
  },
  campuses: {
    all: ['campuses'],
  },
  assessments: {
    all: ['assessments'],
  },
  invoices: {
    all: ['invoices'],
  },
  attendance: {
    all: ['attendance'],
  },
  core_modules: {
    all: ['core_modules'],
  },
  groups: {
    all: ['groups'],
  },
  stats: {
    all: ['stats'],
    model: (modelName) => ['stats', modelName],
  }
};
