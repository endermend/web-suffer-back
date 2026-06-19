<template>
  <main>
    <div class="main_contents">
      <div class="page_hero">
        <h1 class="page_title">Настройки</h1>
        <p class="page_subtitle">Управление почтой и паролем аккаунта</p>
      </div>

      <!-- email card -->
      <div
        ref="emailCardRef"
        class="card settings_card"
        :class="{ shake: isEmailFormShaking }"
        @animationend="isEmailFormShaking = false"
      >
        <div class="card_header">
          <div>
            <span class="card_title">Email</span>
            <p class="card_subtitle">Текущий адрес: {{ currentEmail }}</p>
          </div>
        </div>

        <div
          class="input_wrapper"
          :class="{ field_error: emailFieldErrors.newEmail, shake: isEmailFieldShaking }"
          @animationend="isEmailFieldShaking = false"
        >
          <input
            type="email"
            v-model="emailForm.newEmail"
            @input="emailFieldErrors.newEmail = ''"
            @blur="validateNewEmail(emailForm.newEmail)"
            placeholder="Новый email"
          />
          <transition name="fade">
            <span v-if="emailFieldErrors.newEmail" class="inline_error">{{
              emailFieldErrors.newEmail
            }}</span>
          </transition>
        </div>

        <button type="button" class="primary_btn" @click="handleEmailSave">Сохранить</button>

        <div class="general_error_area">
          <transition name="fade">
            <div v-if="emailFieldErrors.general" class="general_error">
              {{ emailFieldErrors.general }}
            </div>
          </transition>
          <transition name="fade">
            <div v-if="emailSuccess" class="general_success">Email обновлён</div>
          </transition>
        </div>
      </div>

      <!-- password card -->
      <div
        ref="passwordCardRef"
        class="card settings_card"
        :class="{ shake: isPasswordFormShaking }"
        @animationend="isPasswordFormShaking = false"
      >
        <div class="card_header">
          <div>
            <span class="card_title">Пароль</span>
            <p class="card_subtitle">Смена пароля аккаунта</p>
          </div>
        </div>

        <div
          class="input_wrapper"
          :class="{ field_error: passwordFieldErrors.currentPassword, shake: isCurrentPassShaking }"
          @animationend="isCurrentPassShaking = false"
        >
          <input
            :type="showCurrentPassword ? 'text' : 'password'"
            v-model="passwordForm.currentPassword"
            @input="passwordFieldErrors.currentPassword = ''"
            @blur="validateCurrentPassword(passwordForm.currentPassword)"
            placeholder="Текущий пароль"
          />
          <transition name="fade">
            <span v-if="passwordFieldErrors.currentPassword" class="inline_error">{{
              passwordFieldErrors.currentPassword
            }}</span>
          </transition>
          <button
            type="button"
            class="eye_btn"
            @click="showCurrentPassword = !showCurrentPassword"
            tabindex="-1"
          >
            <EyeOpenIcon v-if="!showCurrentPassword" />
            <EyeClosedIcon v-else />
          </button>
        </div>

        <div
          class="input_wrapper"
          :class="{ field_error: passwordFieldErrors.newPassword, shake: isNewPassShaking }"
          @animationend="isNewPassShaking = false"
        >
          <input
            :type="showNewPassword ? 'text' : 'password'"
            v-model="passwordForm.newPassword"
            @input="
              ((passwordFieldErrors.newPassword = ''), (passwordFieldErrors.repeatPassword = ''))
            "
            @blur="validateNewPassword(passwordForm.newPassword)"
            placeholder="Новый пароль"
          />
          <transition name="fade">
            <span v-if="passwordFieldErrors.newPassword" class="inline_error">{{
              passwordFieldErrors.newPassword
            }}</span>
          </transition>
          <button
            type="button"
            class="eye_btn"
            @click="showNewPassword = !showNewPassword"
            tabindex="-1"
          >
            <EyeOpenIcon v-if="!showNewPassword" />
            <EyeClosedIcon v-else />
          </button>
        </div>

        <div
          class="input_wrapper"
          :class="{ field_error: passwordFieldErrors.repeatPassword, shake: isRepeatPassShaking }"
          @animationend="isRepeatPassShaking = false"
        >
          <input
            :type="showRepeatPassword ? 'text' : 'password'"
            v-model="passwordForm.repeatPassword"
            @input="passwordFieldErrors.repeatPassword = ''"
            @blur="validateRepeatPassword(passwordForm.newPassword, passwordForm.repeatPassword)"
            placeholder="Повторите новый пароль"
          />
          <transition name="fade">
            <span v-if="passwordFieldErrors.repeatPassword" class="inline_error">{{
              passwordFieldErrors.repeatPassword
            }}</span>
          </transition>
          <button
            type="button"
            class="eye_btn"
            @click="showRepeatPassword = !showRepeatPassword"
            tabindex="-1"
          >
            <EyeOpenIcon v-if="!showRepeatPassword" />
            <EyeClosedIcon v-else />
          </button>
        </div>

        <button type="button" class="primary_btn" @click="handlePasswordSave">Сохранить</button>

        <div class="general_error_area">
          <transition name="fade">
            <div v-if="passwordFieldErrors.general" class="general_error">
              {{ passwordFieldErrors.general }}
            </div>
          </transition>
          <transition name="fade">
            <div v-if="passwordSuccess" class="general_success">Пароль обновлён</div>
          </transition>
        </div>
      </div>
    </div>
  </main>
</template>

<script setup lang="ts">
import { ref, reactive, nextTick, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth_store.ts'
import EyeOpenIcon from '@/assets/icons/eye-open.svg'
import EyeClosedIcon from '@/assets/icons/eye-closed.svg'

defineOptions({ name: 'SettingsPage' })

const route = useRoute()
const authStore = useAuthStore()

const currentEmail = ref(authStore.userEmail ?? '')

const emailCardRef = ref<HTMLDivElement | null>(null)
const passwordCardRef = ref<HTMLDivElement | null>(null)

onMounted(function () {
  if (route.query.section === 'email') {
    emailCardRef.value?.scrollIntoView({ behavior: 'smooth', block: 'start' })
  } else if (route.query.section === 'password') {
    passwordCardRef.value?.scrollIntoView({ behavior: 'smooth', block: 'start' })
  }
})

// --- email form ---

const emailForm = reactive({ newEmail: '' })
const emailFieldErrors = reactive({ newEmail: '', general: '' })
const isEmailFormShaking = ref(false)
const isEmailFieldShaking = ref(false)
const emailSuccess = ref(false)

type EmailShakeTarget = 'form' | 'field'

function validateNewEmail(str: string): void {
  emailFieldErrors.newEmail = ''

  if (!str.length) {
    emailFieldErrors.newEmail = 'Обязательное поле'
    triggerEmailShake('field')
    return
  }

  const pattern = /[a-zA-Z0-9]+@[a-zA-Z0-9]+\.[a-zA-Z0-9]{2,}$/
  if (!pattern.test(str)) {
    emailFieldErrors.newEmail = 'Неверный email'
    triggerEmailShake('field')
    return
  }
}

async function triggerEmailShake(target: EmailShakeTarget): Promise<void> {
  isEmailFormShaking.value = false
  isEmailFieldShaking.value = false

  await nextTick()

  if (target === 'form') isEmailFormShaking.value = true
  else isEmailFieldShaking.value = true
}

function handleEmailSave(): void {
  emailFieldErrors.general = ''
  emailSuccess.value = false

  validateNewEmail(emailForm.newEmail)

  if (emailFieldErrors.newEmail) {
    return
  }

  // TODO: replace with API call
  authStore.userEmail = emailForm.newEmail
  localStorage.setItem('user_email', emailForm.newEmail)
  currentEmail.value = emailForm.newEmail
  emailForm.newEmail = ''
  emailSuccess.value = true
}

// --- password form ---

const passwordForm = reactive({ currentPassword: '', newPassword: '', repeatPassword: '' })
const passwordFieldErrors = reactive({
  currentPassword: '',
  newPassword: '',
  repeatPassword: '',
  general: '',
})
const showCurrentPassword = ref(false)
const showNewPassword = ref(false)
const showRepeatPassword = ref(false)
const isPasswordFormShaking = ref(false)
const isCurrentPassShaking = ref(false)
const isNewPassShaking = ref(false)
const isRepeatPassShaking = ref(false)
const passwordSuccess = ref(false)

type PasswordShakeTarget = 'form' | 'current' | 'new' | 'repeat'

function validateCurrentPassword(str: string): void {
  passwordFieldErrors.currentPassword = ''

  if (!str.length) {
    passwordFieldErrors.currentPassword = 'Обязательное поле'
    triggerPasswordShake('current')
  }
}

function validateNewPassword(str: string): void {
  passwordFieldErrors.newPassword = ''

  if (!str.length) {
    passwordFieldErrors.newPassword = 'Обязательное поле'
    triggerPasswordShake('new')
    return
  }

  if (str.length < 12) {
    passwordFieldErrors.newPassword = 'Мин. 12 символов'
    triggerPasswordShake('new')
    return
  }

  if (!/[a-z]/.test(str) || !/[A-Z]/.test(str)) {
    passwordFieldErrors.newPassword = 'Нужны заглавные и строчные буквы'
    triggerPasswordShake('new')
    return
  }

  if (!/[^a-zA-Z0-9\s]/.test(str) || !/[0-9]/.test(str)) {
    passwordFieldErrors.newPassword = 'Нужны символы и цифры'
    triggerPasswordShake('new')
    return
  }
}

function validateRepeatPassword(newPass: string, repeat: string): void {
  passwordFieldErrors.repeatPassword = ''

  if (!repeat.length) {
    passwordFieldErrors.repeatPassword = 'Обязательное поле'
    triggerPasswordShake('repeat')
    return
  }

  if (newPass !== repeat) {
    passwordFieldErrors.repeatPassword = 'Не совпадают'
    triggerPasswordShake('repeat')
    return
  }
}

async function triggerPasswordShake(target: PasswordShakeTarget): Promise<void> {
  isPasswordFormShaking.value = false
  isCurrentPassShaking.value = false
  isNewPassShaking.value = false
  isRepeatPassShaking.value = false

  await nextTick()

  switch (target) {
    case 'form':
      isPasswordFormShaking.value = true
      break

    case 'current':
      isCurrentPassShaking.value = true
      break

    case 'new':
      isNewPassShaking.value = true
      break

    case 'repeat':
      isRepeatPassShaking.value = true
      break
  }
}

function handlePasswordSave(): void {
  passwordFieldErrors.general = ''
  passwordSuccess.value = false

  validateCurrentPassword(passwordForm.currentPassword)
  validateNewPassword(passwordForm.newPassword)
  validateRepeatPassword(passwordForm.newPassword, passwordForm.repeatPassword)

  const hasErrors =
    passwordFieldErrors.currentPassword ||
    passwordFieldErrors.newPassword ||
    passwordFieldErrors.repeatPassword

  if (hasErrors) {
    return
  }

  // TODO: replace with API call
  passwordForm.currentPassword = ''
  passwordForm.newPassword = ''
  passwordForm.repeatPassword = ''
  passwordSuccess.value = true
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

/* cards */

.card {
  background-color: white;
  border-radius: 16px;
  box-shadow: 0px 0px 15px 0px rgb(0, 0, 0, 0.2);
  padding: 24px;
}

.settings_card {
  display: flex;
  flex-direction: column;
  max-width: 480px;
}

.card_header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 20px;
}

.card_title {
  font-family: Nagel;
  font-size: 18px;
  color: rgb(65, 65, 65);
  display: block;
  margin-bottom: 4px;
}

.card_subtitle {
  font-family: Nagel;
  font-size: 13px;
  color: rgb(150, 150, 150);
  margin: 0;
}

/* fields */

input,
button {
  appearance: none;
  background: none;
  border: none;
  outline: none;
}

.input_wrapper {
  display: flex;
  align-items: center;
  border: thin solid rgb(180, 180, 180);
  border-radius: 16px;
  margin-block: 0.4rem;
  overflow: hidden;
  transition: border-color 0.15s;
}

.input_wrapper.field_error {
  border-color: rgb(204, 63, 75);
}

.input_wrapper input {
  flex: 1;
  min-width: 0;
  padding: 14px 16px;
  font-size: 16px;
  font-family: Nagel;
}

.inline_error {
  flex-shrink: 0;
  padding-right: 8px;
  font-size: 11px;
  color: rgb(204, 63, 75);
  font-family: Nagel;
  max-width: 96px;
  line-height: 1.3;
  text-align: right;
}

.eye_btn {
  flex-shrink: 0;
  align-self: stretch;
  padding-inline: 12px;
  display: flex;
  align-items: center;
  cursor: pointer;
  color: rgb(170, 170, 170);
  transition: color 0.15s;
}

.eye_btn:hover {
  color: rgb(160, 125, 180);
}

.eye_btn svg {
  width: 18px;
  height: 18px;
}

/* buttons */

.primary_btn {
  align-self: flex-start;
  background-color: white;
  border: thin solid black;
  font-size: 16px;
  margin-top: 0.6rem;
  padding: 10px 20px;
  border-radius: 16px;
  transition:
    0.2s background-color,
    border,
    color;
  font-family: Nagel;
  cursor: pointer;
}

.primary_btn:hover {
  background-color: rgb(160, 125, 180);
  border: thin solid rgb(160, 125, 180);
  color: white;
}

/* general error / success */

.general_error_area {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-top: 12px;
}

.general_error {
  width: 100%;
  box-sizing: border-box;
  background-color: rgb(204, 63, 75);
  color: white;
  font-size: 14px;
  font-family: Nagel;
  padding: 10px 12px;
  border-radius: 12px;
}

.general_success {
  width: 100%;
  box-sizing: border-box;
  background-color: rgb(22, 163, 74);
  color: white;
  font-size: 14px;
  font-family: Nagel;
  padding: 10px 12px;
  border-radius: 12px;
}

/* transitions */

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* shake animation */

@keyframes shake {
  0%,
  100% {
    transform: translateX(0);
  }
  20% {
    transform: translateX(-8px);
  }
  40% {
    transform: translateX(8px);
  }
  60% {
    transform: translateX(-5px);
  }
  80% {
    transform: translateX(5px);
  }
}

.shake {
  animation: shake 0.4s ease-in-out;
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

  .settings_card {
    max-width: 100%;
  }
}
</style>
