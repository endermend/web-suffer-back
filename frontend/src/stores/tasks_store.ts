import { defineStore } from 'pinia'
import type { Task } from '@/types/tasks.ts'

const useTasksStore = defineStore('tasks', {
  state: () => ({
    // TODO: replace with API call
    tasks: [
      {
        id: 1,
        title: 'Орг. встреча волонтёров',
        description: 'Подготовить план мероприятия и список участников',
        deadline: '2026-06-25T18:00:00',
        points: 40,
        answer: '',
        submission_files: [],
        status: 'available',
      },
      {
        id: 2,
        title: 'Фотоотчёт с акции',
        description: 'Загрузить фото и короткое описание прошедшей акции',
        deadline: '2026-06-28T23:59:00',
        points: 30,
        answer: '',
        submission_files: [],
        status: 'available',
      },
      {
        id: 3,
        title: 'Анкета участника форума',
        description: 'Заполнить анкету для участия в молодёжном форуме',
        deadline: '2026-07-02T12:00:00',
        points: 20,
        answer: '',
        submission_files: [],
        status: 'available',
      },
      {
        id: 4,
        title: 'Эссе о волонтёрстве',
        description: 'Написать эссе на 1-2 страницы о личном опыте волонтёрства',
        deadline: '2026-07-05T20:00:00',
        points: 50,
        answer: '',
        submission_files: [],
        status: 'available',
      },
      {
        id: 5,
        title: 'Регистрация на слёт',
        description: 'Подать заявку на участие в летнем слёте движения',
        deadline: '2026-06-20T12:00:00',
        points: 15,
        answer: 'Заявка отправлена, жду подтверждения',
        submission_files: [],
        status: 'submitted',
        submitted_at: '2026-06-18T10:00:00',
        submitted_by: 'denis.korolev@mail.ru',
      },
      {
        id: 6,
        title: 'Отчёт по субботнику',
        description: 'Прислать отчёт о проведённом субботнике с фото',
        deadline: '2026-06-15T18:00:00',
        points: 25,
        answer: 'Отчёт во вложении, субботник прошёл успешно',
        submission_files: [],
        status: 'submitted',
        submitted_at: '2026-06-14T19:00:00',
        submitted_by: 'endermend1@mail.ru',
      },
      {
        id: 7,
        title: 'Мероприятие 1',
        description: 'Организация и проведение мероприятия для участников движения',
        deadline: '2024-02-15T10:00:00',
        points: 95,
        answer: 'Мероприятие проведено, отчёт приложен',
        submission_files: [],
        status: 'graded',
        submitted_at: '2024-02-15T10:00:00',
        submitted_by: 'denis.korolev@mail.ru',
      },
      {
        id: 8,
        title: 'Мероприятие 2',
        description: 'Помощь в организации второго мероприятия',
        deadline: '2024-02-22T14:30:00',
        points: 78,
        answer: 'Задача выполнена',
        submission_files: [],
        status: 'graded',
        submitted_at: '2024-02-22T14:30:00',
        submitted_by: 'anna.smirnova@example.com',
      },
      {
        id: 9,
        title: 'Практическое задание',
        description: 'Выполнение практического задания по организации волонтёрства',
        deadline: '2024-03-05T09:15:00',
        points: 88,
        answer: 'Выполнено',
        submission_files: [],
        status: 'graded',
        submitted_at: '2024-03-05T09:15:00',
        submitted_by: 'maria.k@example.com',
      },
      {
        id: 10,
        title: 'Выступление',
        description: 'Подготовка и проведение выступления на форуме',
        deadline: '2024-03-18T11:00:00',
        points: 42,
        answer: 'Выступление прошло',
        submission_files: [],
        status: 'graded',
        submitted_at: '2024-03-18T11:00:00',
        submitted_by: 'denis.korolev@mail.ru',
      },
      {
        id: 11,
        title: 'Проведение мероприятия',
        description: 'Организация мероприятия для местного сообщества',
        deadline: '2024-04-01T16:00:00',
        points: 91,
        answer: 'Готово',
        submission_files: [],
        status: 'graded',
        submitted_at: '2024-04-01T16:00:00',
        submitted_by: 'endermend1@mail.ru',
      },
    ] as Task[],
  }),

  getters: {
    availableTasks: (state) => state.tasks.filter((t) => t.status === 'available'),
    pendingTasks: (state) => state.tasks.filter((t) => t.status === 'submitted'),
    completedTasks: (state) => state.tasks.filter((t) => t.status === 'graded'),
    rejectedTasks: (state) => state.tasks.filter((t) => t.status === 'rejected'),
  },

  actions: {
    updateAnswer(id: number, answer: string) {
      const task = this.tasks.find((t) => t.id === id)
      if (task) task.answer = answer
    },

    addSubmissionFile(id: number, file: File) {
      const task = this.tasks.find((t) => t.id === id)
      if (!task) return
      const fileId = task.submission_files.length
        ? Math.max(...task.submission_files.map((f) => f.id)) + 1
        : 1
      task.submission_files.push({ id: fileId, name: file.name, url: URL.createObjectURL(file) })
    },

    removeSubmissionFile(id: number, fileId: number) {
      const task = this.tasks.find((t) => t.id === id)
      if (!task) return
      task.submission_files = task.submission_files.filter((f) => f.id !== fileId)
    },

    // TODO: replace with API call
    submitTask(id: number, submittedBy: string) {
      const task = this.tasks.find((t) => t.id === id)
      if (!task || (task.status !== 'available' && task.status !== 'rejected')) return
      task.status = 'submitted'
      task.submitted_at = new Date().toISOString()
      task.submitted_by = submittedBy
    },

    // TODO: replace with API call
    createTask(data: { title: string; description: string; deadline: string; points: number }) {
      const id = this.tasks.length ? Math.max(...this.tasks.map((t) => t.id)) + 1 : 1
      this.tasks.push({
        id,
        title: data.title,
        description: data.description,
        deadline: data.deadline,
        points: data.points,
        answer: '',
        submission_files: [],
        status: 'available',
      })
    },

    // TODO: replace with API call
    // points are fixed at task creation — grading just confirms the submission, it doesn't assign a score
    gradeTask(id: number, comment: string) {
      const task = this.tasks.find((t) => t.id === id)
      if (!task || task.status !== 'submitted') return
      task.status = 'graded'
      task.admin_comment = comment
    },

    // TODO: replace with API call
    rejectTask(id: number, comment: string) {
      const task = this.tasks.find((t) => t.id === id)
      if (!task || task.status !== 'submitted') return
      task.status = 'rejected'
      task.admin_comment = comment
    },
  },
})

export { useTasksStore }