<template>
  <main>
    <div class="main_contents page_enter">
      <div class="page_hero">
        <h1 class="page_title">Пользователи</h1>
        <p class="page_subtitle">Поиск и управление пользователями</p>
      </div>

      <div class="card">
        <input v-model="searchQuery" class="search_input" placeholder="Поиск по email..." />

        <div v-if="filteredUsers.length" class="users_list">
          <div v-for="user in filteredUsers" :key="user.id" class="user_row">
            <div class="user_main">
              <span class="user_email">{{ user.email }}</span>
              <span
                class="status_chip"
                :class="user.status === 'banned' ? 'chip_banned' : 'chip_active'"
              >
                {{ user.status === 'banned' ? 'Забанен' : 'Активен' }}
              </span>
              <select class="role_select" :value="user.role" @change="changeRole(user, $event)">
                <option value="user">Участник</option>
                <option value="moderator">Модератор</option>
                <option value="admin">Админ</option>
              </select>
            </div>

            <div class="user_actions">
              <button class="action_btn" @click="toggleBan(user)">
                {{ user.status === 'banned' ? 'Разбанить' : 'Забанить' }}
              </button>
              <button class="action_btn" @click="startEdit(user, 'email')">Сменить почту</button>
              <button class="action_btn" @click="startEdit(user, 'password')">
                Сменить пароль
              </button>
              <button class="action_btn action_btn_danger" @click="deleteUser(user)">
                Удалить
              </button>
            </div>

            <div v-if="editingUserId === user.id" class="edit_panel">
              <input
                v-model="editValue"
                :type="editingField === 'password' ? 'text' : 'email'"
                :placeholder="editingField === 'password' ? 'Новый пароль' : 'Новый email'"
                class="edit_input"
              />
              <button class="action_btn action_btn_primary" @click="saveEdit(user)">
                Сохранить
              </button>
              <button class="action_btn" @click="cancelEdit">Отмена</button>
            </div>
          </div>
        </div>
        <div v-else-if="usersStore.loading" class="empty_state">Загрузка...</div>
        <div v-else class="empty_state">Пользователи не найдены</div>
      </div>
    </div>
  </main>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useUsersStore } from '@/stores/users_store.ts'
import type { ApiUserRole } from '@/types/auth.ts'
import type { UserManagement } from '@/types/users.ts'

defineOptions({ name: 'UsersPage' })

const usersStore = useUsersStore()

onMounted(function () {
  usersStore.fetchUsers()
})

const searchQuery = ref('')

const filteredUsers = computed(function () {
  return usersStore.users.filter(function (user) {
    return user.email.toLowerCase().includes(searchQuery.value.toLowerCase())
  })
})

function toggleBan(user: UserManagement): void {
  usersStore.setStatus(user.id, user.status === 'banned' ? 'active' : 'banned')
}

function changeRole(user: UserManagement, event: Event): void {
  const role = (event.target as HTMLSelectElement).value as ApiUserRole
  usersStore.setRole(user.id, role)
}

function deleteUser(user: UserManagement): void {
  usersStore.deleteUser(user.id)
}

const editingUserId = ref<string | null>(null)
const editingField = ref<'email' | 'password' | null>(null)
const editValue = ref('')

function startEdit(user: UserManagement, field: 'email' | 'password'): void {
  editingUserId.value = user.id
  editingField.value = field
  editValue.value = field === 'email' ? user.email : ''
}

function cancelEdit(): void {
  editingUserId.value = null
  editingField.value = null
  editValue.value = ''
}

function saveEdit(user: UserManagement): void {
  if (editingField.value === 'email') {
    usersStore.updateEmail(user.id, editValue.value)
  } else if (editingField.value === 'password') {
    usersStore.updatePassword(user.id, editValue.value)
  }
  cancelEdit()
}
</script>

<style scoped>
main {
  box-sizing: border-box;
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  background-color: rgb(244, 243, 250);
  min-height: 100vh;
}

.main_contents {
  padding-top: calc(100px + 70px);
  padding-bottom: 48px;
  width: 1000px;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

/* hero */

.page_hero {
  margin-top: 32px;
}

.page_title {
  font-family: Nagel;
  font-size: 2rem;
  color: rgb(65, 65, 65);
  margin: 0 0 6px;
}

.page_subtitle {
  font-family: Nagel;
  font-size: 14px;
  color: rgb(150, 150, 150);
  margin: 0;
}

/* card */

.card {
  background-color: white;
  border-radius: 16px;
  box-shadow: 0px 0px 15px 0px rgb(0, 0, 0, 0.2);
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

/* search */

.search_input {
  appearance: none;
  border: thin solid rgb(210, 208, 220);
  border-radius: 10px;
  padding: 10px 14px;
  font-family: Nagel;
  font-size: 14px;
  color: rgb(65, 65, 65);
  background-color: white;
  outline: none;
  transition: 0.2s border-color;
}

.search_input:focus {
  border-color: rgb(160, 125, 180);
}

/* users list */

.users_list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.user_row {
  display: flex;
  flex-direction: column;
  gap: 10px;
  padding: 14px 16px;
  border-radius: 12px;
  background-color: rgb(244, 243, 250);
}

.user_main {
  display: flex;
  align-items: center;
  gap: 10px;
}

.user_email {
  font-family: Nagel;
  font-size: 15px;
  color: rgb(65, 65, 65);
}

.status_chip {
  display: inline-block;
  padding: 3px 10px;
  border-radius: 999px;
  font-family: Nagel;
  font-size: 12px;
}

.chip_active {
  background-color: rgba(22, 163, 74, 0.12);
  color: rgb(22, 163, 74);
}

.chip_banned {
  background-color: rgba(204, 63, 75, 0.12);
  color: rgb(204, 63, 75);
}

.role_select {
  appearance: none;
  border: thin solid rgb(210, 208, 220);
  border-radius: 999px;
  padding: 3px 10px;
  font-family: Nagel;
  font-size: 12px;
  color: rgb(65, 65, 65);
  background-color: white;
  outline: none;
  cursor: pointer;
  margin-left: auto;
  transition: 0.2s border-color;
}

.role_select:focus {
  border-color: rgb(160, 125, 180);
}

.user_actions {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.action_btn {
  appearance: none;
  border: thin solid rgb(210, 208, 220);
  border-radius: 10px;
  padding: 6px 14px;
  font-family: Nagel;
  font-size: 13px;
  cursor: pointer;
  background-color: white;
  color: rgb(65, 65, 65);
  transition: 0.2s background-color;
}

.action_btn:hover {
  background-color: rgb(235, 232, 242);
}

.action_btn_primary {
  background-color: rgb(160, 125, 180);
  border-color: rgb(160, 125, 180);
  color: white;
}

.action_btn_primary:hover {
  background-color: rgb(140, 105, 160);
}

.action_btn_danger {
  color: rgb(204, 63, 75);
  border-color: rgb(204, 63, 75);
}

.action_btn_danger:hover {
  background-color: rgba(204, 63, 75, 0.1);
}

/* edit panel */

.edit_panel {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.edit_input {
  appearance: none;
  border: thin solid rgb(210, 208, 220);
  border-radius: 10px;
  padding: 6px 14px;
  font-family: Nagel;
  font-size: 13px;
  color: rgb(65, 65, 65);
  outline: none;
  flex: 1;
  min-width: 160px;
  transition: 0.2s border-color;
}

.edit_input:focus {
  border-color: rgb(160, 125, 180);
}

.empty_state {
  padding: 32px 16px;
  text-align: center;
  font-family: Nagel;
  color: rgb(150, 150, 150);
  font-size: 14px;
}

/* responsive */

@media screen and (max-width: 1050px) {
  main {
    padding-inline: 16px;
  }

  .main_contents {
    width: 100%;
  }
}

@media screen and (max-width: 540px) {
  .main_contents {
    padding-top: 70px;
  }
}
</style>
