import { defineStore } from 'pinia'
import type { Submission, SubmissionStatus, Task, UserTask } from '@/types/tasks.ts'

// Mirrors the backend's status priority (task_repository.py get_list): when a user has
// multiple submissions for the same task, the "current" one is picked in this order.
const SUBMISSION_PRIORITY: Record<SubmissionStatus, number> = {
  accepted: 1,
  pending: 2,
  rejected: 3,
}

function resolveCurrentSubmission(submissions: Submission[]): Submission | undefined {
  if (!submissions.length) return undefined
  return [...submissions].sort((a, b) => {
    const diff = SUBMISSION_PRIORITY[a.status] - SUBMISSION_PRIORITY[b.status]
    if (diff !== 0) return diff
    return new Date(b.submitted_at).getTime() - new Date(a.submitted_at).getTime()
  })[0]
}

const useTasksStore = defineStore('tasks', {
  state: () => ({
    // TODO: replace with API call
    // Task templates only — no per-user state here, matches the backend's Task entity.
    tasks: [
      {
        id: 1,
        title: 'Орг. встреча волонтёров',
        description:
          'Подготовить подробный план мероприятия: список участников, распределение ролей и зон ответственности, тайминг встречи по минутам, бронирование помещения и согласование с кураторами движения.',
        deadline: '2026-06-25T18:00:00',
        exp: 40,
        money: 0,
      },
      {
        id: 2,
        title: 'Фотоотчёт с акции',
        description: 'Загрузить фото и короткое описание прошедшей акции.',
        deadline: '2026-06-28T23:59:00',
        exp: 30,
        money: 0,
      },
      {
        id: 3,
        title: 'Анкета участника форума',
        description:
          'Заполнить анкету для участия в молодёжном форуме: ФИО, контакты, направление, ожидания от участия и краткий рассказ о своём опыте волонтёрства.',
        deadline: '2026-07-02T12:00:00',
        exp: 20,
        money: 0,
      },
      {
        id: 4,
        title: 'Эссе о волонтёрстве',
        description:
          'Написать эссе на 1-2 страницы о личном опыте волонтёрства: что мотивировало присоединиться к движению, какие задачи запомнились больше всего и как этот опыт повлиял на дальнейшие планы.',
        deadline: '2026-07-05T20:00:00',
        exp: 50,
        money: 0,
      },
      {
        id: 5,
        title: 'Регистрация на слёт',
        description: 'Подать заявку на участие в летнем слёте движения.',
        deadline: '2026-06-20T12:00:00',
        exp: 15,
        money: 0,
      },
      {
        id: 6,
        title: 'Отчёт по субботнику',
        description:
          'Прислать отчёт о проведённом субботнике: фото до и после, количество участников, список собранного мусора и краткие впечатления от мероприятия.',
        deadline: '2026-06-15T18:00:00',
        exp: 25,
        money: 0,
      },
      {
        id: 7,
        title: 'Мероприятие 1',
        description: 'Организация и проведение мероприятия для участников движения.',
        deadline: '2024-02-15T10:00:00',
        exp: 95,
        money: 0,
      },
      {
        id: 8,
        title: 'Мероприятие 2',
        description:
          'Помощь в организации второго мероприятия: встреча гостей, координация волонтёров на площадке, контроль тайминга программы и помощь с техническим оснащением сцены.',
        deadline: '2024-02-22T14:30:00',
        exp: 78,
        money: 0,
      },
      {
        id: 9,
        title: 'Практическое задание',
        description: 'Выполнение практического задания по организации волонтёрства.',
        deadline: '2024-03-05T09:15:00',
        exp: 88,
        money: 0,
      },
      {
        id: 10,
        title: 'Выступление',
        description:
          'Подготовка и проведение выступления на форуме: тема по выбору участника, регламент 10 минут, презентация и ответы на вопросы аудитории после доклада.',
        deadline: '2024-03-18T11:00:00',
        exp: 42,
        money: 0,
      },
      {
        id: 11,
        title: 'Проведение мероприятия',
        description: 'Организация мероприятия для местного сообщества.',
        deadline: '2024-04-01T16:00:00',
        exp: 91,
        money: 0,
      },
    ] as Task[],

    // TODO: replace with API call
    // One row per attempt. A user can have several submissions for the same task
    // (e.g. rejected, then resubmitted) — the current one is resolved by priority.
    submissions: [
      {
        id: 1,
        task_id: 5,
        user_email: 'denis.korolev@mail.ru',
        content: 'Заявка отправлена, жду подтверждения',
        file: null,
        status: 'pending',
        admin_comment: '',
        submitted_at: '2026-06-18T10:00:00',
      },
      {
        id: 2,
        task_id: 6,
        user_email: 'endermend1@mail.ru',
        content: 'Отчёт во вложении, субботник прошёл успешно',
        file: null,
        status: 'pending',
        admin_comment: '',
        submitted_at: '2026-06-14T19:00:00',
      },
      {
        id: 3,
        task_id: 7,
        user_email: 'denis.korolev@mail.ru',
        content: 'Мероприятие проведено, отчёт приложен',
        file: null,
        status: 'accepted',
        admin_comment: '',
        submitted_at: '2024-02-15T10:00:00',
      },
      {
        id: 4,
        task_id: 8,
        user_email: 'anna.smirnova@example.com',
        content: 'Задача выполнена',
        file: null,
        status: 'accepted',
        admin_comment: '',
        submitted_at: '2024-02-22T14:30:00',
      },
      {
        id: 5,
        task_id: 9,
        user_email: 'maria.k@example.com',
        content: 'Выполнено',
        file: null,
        status: 'accepted',
        admin_comment: '',
        submitted_at: '2024-03-05T09:15:00',
      },
      {
        id: 6,
        task_id: 10,
        user_email: 'denis.korolev@mail.ru',
        content: 'Выступление прошло',
        file: null,
        status: 'accepted',
        admin_comment: '',
        submitted_at: '2024-03-18T11:00:00',
      },
      {
        id: 7,
        task_id: 11,
        user_email: 'endermend1@mail.ru',
        content: 'Готово',
        file: null,
        status: 'accepted',
        admin_comment: '',
        submitted_at: '2024-04-01T16:00:00',
      },
    ] as Submission[],
  }),

  getters: {
    // Per-user view of every task, joined with that user's current submission — mirrors
    // the backend's get_list() SQL join. Status defaults to "available" with no submission.
    userTasks:
      (state) =>
      (userEmail: string): UserTask[] =>
        state.tasks.map((task) => {
          const mine = state.submissions.filter(
            (s) => s.task_id === task.id && s.user_email === userEmail,
          )
          const current = resolveCurrentSubmission(mine)
          return { ...task, status: current?.status ?? 'available' }
        }),

    // The submission currently representing a user's attempt at one task (if any).
    mySubmissionForTask:
      (state) =>
      (taskId: number, userEmail: string): Submission | undefined =>
        resolveCurrentSubmission(
          state.submissions.filter((s) => s.task_id === taskId && s.user_email === userEmail),
        ),

    // All submissions waiting on admin review, across every user.
    pendingSubmissions: (state) => state.submissions.filter((s) => s.status === 'pending'),

    // A user's accepted submissions joined with their task, newest first — used wherever
    // we need submission metadata (submitted_at) alongside the task, e.g. profile stats
    // and the "recently graded" list. UserTask alone doesn't carry this (neither does the
    // backend's UsersTaskDTO — that ordering is a query param there, not an extra field).
    acceptedSubmissionsWithTask:
      (state) =>
      (userEmail: string): Array<{ task: Task; submission: Submission }> =>
        state.submissions
          .filter((s) => s.user_email === userEmail && s.status === 'accepted')
          .map((submission) => {
            const task = state.tasks.find((t) => t.id === submission.task_id)
            return task ? { task, submission } : null
          })
          .filter((entry): entry is { task: Task; submission: Submission } => entry !== null)
          .sort(
            (a, b) =>
              new Date(b.submission.submitted_at).getTime() -
              new Date(a.submission.submitted_at).getTime(),
          ),
  },

  actions: {
    // TODO: replace with API call
    createTask(data: {
      title: string
      description: string
      deadline: string
      exp: number
      money: number
    }) {
      const id = this.tasks.length ? Math.max(...this.tasks.map((t) => t.id)) + 1 : 1
      this.tasks.push({ id, ...data })
    },

    // TODO: replace with API call
    // Creates a new attempt — used for both the first submission and any resubmission
    // after a rejection. The old rejected row is kept as history, not overwritten.
    createSubmission(taskId: number, userEmail: string, content: string, file: File | null) {
      const id = this.submissions.length ? Math.max(...this.submissions.map((s) => s.id)) + 1 : 1
      this.submissions.push({
        id,
        task_id: taskId,
        user_email: userEmail,
        content,
        file: file ? { name: file.name, url: URL.createObjectURL(file) } : null,
        status: 'pending',
        admin_comment: '',
        submitted_at: new Date().toISOString(),
      })
    },

    // TODO: replace with API call
    acceptSubmission(submissionId: number, comment: string) {
      const submission = this.submissions.find((s) => s.id === submissionId)
      if (!submission || submission.status !== 'pending') return
      submission.status = 'accepted'
      submission.admin_comment = comment
    },

    // TODO: replace with API call
    rejectSubmission(submissionId: number, comment: string) {
      const submission = this.submissions.find((s) => s.id === submissionId)
      if (!submission || submission.status !== 'pending') return
      submission.status = 'rejected'
      submission.admin_comment = comment
    },
  },
})

export { useTasksStore }
