import type { UserTaskStatus } from '@/types/tasks.ts'

function formatDateShort(str: string): string {
  return new Date(str).toLocaleDateString('ru-RU', {
    day: 'numeric',
    month: 'short',
    hour: '2-digit',
    minute: '2-digit',
  })
}

function formatDateLong(str: string): string {
  return new Date(str).toLocaleString('ru-RU', {
    day: 'numeric',
    month: 'long',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })
}

// CSS class names keep their old wording (chip_graded etc.) — they're purely visual
// and already used across several components' <style> blocks, no need to churn those.
function statusChip(status: UserTaskStatus): string {
  if (status === 'accepted') return 'chip_graded'
  if (status === 'pending') return 'chip_submitted'
  if (status === 'rejected') return 'chip_rejected'
  return 'chip_assigned'
}

function statusLabel(status: UserTaskStatus): string {
  if (status === 'accepted') return 'Проверено'
  if (status === 'pending') return 'Сдано'
  if (status === 'rejected') return 'Отклонено'
  return 'Доступно'
}

export { formatDateShort, formatDateLong, statusChip, statusLabel }
