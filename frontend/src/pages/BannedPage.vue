<template>
  <div class="auth_form">
    <span class="not_found_text">Этот аккаунт временно заблокирован</span>
    <button type="button" class="primary_btn" @click="router.push('/')">На главную</button>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'

defineOptions({ name: 'BannedPage' })

const router = useRouter()
</script>

<style scoped>
.auth_form {
  width: 400px;
  display: flex;
  flex-direction: column;
  align-items: center;
  background-color: white;
  padding: 24px;
  margin-top: 200px;
  margin-bottom: 40px;
  border-radius: 16px;
  font-family: Nagel;
  box-shadow: 0px 0px 30px 0px rgb(0, 0, 0, 0.2);
}

.not_found_text {
  font-size: 16px;
  color: rgb(150, 150, 150);
  margin-top: 12px;
  margin-bottom: 24px;
  text-align: center;
}

.primary_btn {
  appearance: none;
  background-color: white;
  border: thin solid black;
  font-size: 20px;
  padding: 10px 24px;
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

@media screen and (max-width: 440px) {
  .auth_form {
    width: calc(100vw - 32px);
    margin-top: 200px;
  }
}
</style>
