<template>
  <form
    @submit.prevent="handleSignUp"
    class="auth_form"
    :class="{ shake: isFormShaking }"
    @animationend="isFormShaking = false"
    novalidate
  >
    <span class="auth_form_header">Регистрация</span>

    <!-- email -->

    <div
      class="input_wrapper"
      :class="{ field_error: fieldErrors.email, shake: isEmailShaking }"
      @animationend="isEmailShaking = false"
    >
      <input
        type="email"
        v-model="form.email"
        @input="fieldErrors.email = ''"
        @blur="validateEmail(form.email)"
        placeholder="Почта"
      />
      <transition name="fade">
        <span v-if="fieldErrors.email" class="inline_error">{{ fieldErrors.email }}</span>
      </transition>
    </div>

    <!-- password -->

    <div
      class="input_wrapper"
      :class="{ field_error: fieldErrors.password, shake: isPassShaking }"
      @animationend="isPassShaking = false"
    >
      <input
        :type="showPassword ? 'text' : 'password'"
        v-model="form.password"
        @blur="validatePass(form.password)"
        @input="((fieldErrors.password = ''), (fieldErrors.password_repeat = ''))"
        placeholder="Пароль"
      />
      <transition name="fade">
        <span v-if="fieldErrors.password" class="inline_error">{{ fieldErrors.password }}</span>
      </transition>
      <button type="button" class="eye_btn" @click="showPassword = !showPassword" tabindex="-1">
        <EyeOpenIcon v-if="!showPassword" />
        <EyeClosedIcon v-else />
      </button>
    </div>

    <!-- repeat  -->

    <div
      class="input_wrapper"
      :class="{ field_error: fieldErrors.password_repeat, shake: isRepeatShaking }"
      @animationend="isRepeatShaking = false"
    >
      <input
        :type="showPasswordRepeat ? 'text' : 'password'"
        v-model="form.password_repeat"
        @blur="validateRepeat(form.password, form.password_repeat)"
        @input="fieldErrors.password_repeat = ''"
        placeholder="Повторение пароля"
      />
      <transition name="fade">
        <span v-if="fieldErrors.password_repeat" class="inline_error">{{
          fieldErrors.password_repeat
        }}</span>
      </transition>
      <button
        type="button"
        class="eye_btn"
        @click="showPasswordRepeat = !showPasswordRepeat"
        tabindex="-1"
      >
        <EyeOpenIcon v-if="!showPasswordRepeat" />
        <EyeClosedIcon v-else />
      </button>
    </div>

    <button type="submit" class="primary_btn">Зарегистрироваться</button>
    <button type="button" @click="router.push('/login')" class="secondary_btn">
      Уже есть аккаунт?
    </button>
  </form>

  <!-- misc errors  -->

  <div class="general_error_area">
    <transition name="fade">
      <div v-if="fieldErrors.general" class="general_error">
        <WarningIcon />
        {{ fieldErrors.general }}
      </div>
    </transition>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth_store.ts'
import EyeOpenIcon from '@/assets/icons/eye-open.svg'
import EyeClosedIcon from '@/assets/icons/eye-closed.svg'
import WarningIcon from '@/assets/icons/warning.svg'

defineOptions({ name: 'RegisterPage' })

const router = useRouter()
const authStore = useAuthStore()

const form = reactive({ email: '', password: '', password_repeat: '' })
const fieldErrors = reactive({ email: '', password: '', password_repeat: '', general: '' })
const showPassword = ref(false)
const showPasswordRepeat = ref(false)
const isFormShaking = ref(false)
const isEmailShaking = ref(false)
const isPassShaking = ref(false)
const isRepeatShaking = ref(false)

type ShakeTarget = 'form' | 'email' | 'pass' | 'repeat'

function validateEmail(str: string): void {
  fieldErrors.email = ''

  if (!str.length) {
    fieldErrors.email = 'Обязательное поле'
    triggerShake('email')
    return
  }

  const pattern = /[a-zA-Z0-9]+@[a-zA-Z0-9]+\.[a-zA-Z0-9]{2,}$/
  if (!pattern.test(str)) {
    fieldErrors.email = 'Неверный email'
    triggerShake('email')
    return
  }
}

function validatePass(str: string): void {
  fieldErrors.password = ''

  if (!str.length) {
    fieldErrors.password = 'Обязательное поле'
    triggerShake('pass')
    return
  }

  if (str.length < 12) {
    fieldErrors.password = 'Мин. 12 символов'
    triggerShake('pass')
    return
  }

  if (!/[a-z]/.test(str) || !/[A-Z]/.test(str)) {
    fieldErrors.password = 'Нужны заглавные и строчные буквы'
    triggerShake('pass')
    return
  }

  if (!/[^a-zA-Z0-9\s]/.test(str) || !/[0-9]/.test(str)) {
    fieldErrors.password = 'Нужны символы и цифры'
    triggerShake('pass')
    return
  }
}

function validateRepeat(pass: string, repeat: string): void {
  fieldErrors.password_repeat = ''

  if (!repeat.length) {
    fieldErrors.password_repeat = 'Обязательное поле'
    triggerShake('repeat')
    return
  }

  if (pass !== repeat) {
    fieldErrors.password_repeat = 'Не совпадают'
    triggerShake('repeat')
    return
  }
}

async function triggerShake(target: ShakeTarget): Promise<void> {
  isFormShaking.value = false
  isEmailShaking.value = false
  isPassShaking.value = false
  isRepeatShaking.value = false

  await nextTick()

  switch (target) {
    case 'form':
      isFormShaking.value = true
      break

    case 'email':
      isEmailShaking.value = true
      break

    case 'pass':
      isPassShaking.value = true
      break

    case 'repeat':
      isRepeatShaking.value = true
      break
  }
}

async function handleSignUp(): Promise<void> {
  fieldErrors.email = ''
  fieldErrors.password = ''
  fieldErrors.password_repeat = ''
  fieldErrors.general = ''

  validateEmail(form.email)
  validatePass(form.password)
  validateRepeat(form.password, form.password_repeat)

  if (authStore.isAuthenticated) {
    fieldErrors.general = 'Вы уже вошли. Сначала выйдите.'
  }

  const hasErrors =
    fieldErrors.email || fieldErrors.password || fieldErrors.password_repeat || fieldErrors.general

  if (hasErrors) {
    return
  }

  try {
    const result = await authStore.register({ email: form.email, password: form.password })
    if (result.success) {
      await authStore.fetchUserEmail()
      router.push('/')
    } else {
      fieldErrors.general = result.error
      triggerShake('form')
    }
  } catch {
    fieldErrors.general = 'Произошла ошибка при регистрации'
  }
}
</script>

<style scoped>
input,
button {
  appearance: none;
  background: none;
  border: none;
  outline: none;
}

.auth_form {
  width: 400px;
  display: flex;
  flex-direction: column;
  background-color: white;
  padding: 24px;
  margin-top: 80px;
  margin-bottom: 40px;
  border-radius: 16px;
  font-family: Nagel;
  box-shadow: 0px 0px 30px 0px rgb(0, 0, 0, 0.2);
}

.auth_form_header {
  font-size: 1.5rem;
  padding: 16px;
  align-self: center;
}

/* fields */

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
  background-color: white;
  border: thin solid black;
  font-size: 20px;
  margin-block: 0.4rem;
  padding: 10px;
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

.secondary_btn {
  transition:
    1s color,
    1s border;
  border: thin solid rgb(130, 130, 130);
  color: rgb(130, 130, 130);
  font-size: 14px;
  margin-block: 0.2rem;
  padding: 6px;
  border-radius: 16px;
  font-family: Nagel;
  cursor: pointer;
  transition: color 0.2s;
}

.secondary_btn:hover {
  color: rgb(160, 125, 180);
  border: thin solid rgb(160, 125, 180);
}

/* general error */

.general_error_area {
  min-height: 46px;
  display: flex;
  align-items: center;
  margin-top: 4px;
}

.general_error {
  width: 100%;
  box-sizing: border-box;
  display: flex;
  align-items: center;
  gap: 6px;
  background-color: rgb(204, 63, 75);
  color: white;
  font-size: 14px;
  font-family: Nagel;
  padding: 10px 12px;
  border-radius: 12px;
}

.general_error svg {
  width: 16px;
  height: 16px;
  flex-shrink: 0;
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

@media screen and (max-width: 440px) {
  .auth_form {
    width: calc(100vw - 32px);
    margin-top: 40px;
  }
}
</style>
