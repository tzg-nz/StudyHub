<template>
  <div style="max-width: 500px; margin: 40px auto;">
    <a-card title="注册新账号">
      <template #extra>
        <router-link to="/login">已有账号？去登录</router-link>
      </template>

      <a-alert
        message="注册后会同时初始化三种认证方式"
        description="注册成功后，后端会同时创建Session、生成JWT Token、设置Cookie，你可以体验三种认证方式的差异。"
        type="info"
        show-icon
        style="margin-bottom: 16px;"
      />

      <a-space direction="vertical" style="width: 100%;" :size="12">
        <a-input v-model:value="formUsername" placeholder="请输入用户名" />
        <a-input v-model:value="formEmail" placeholder="请输入邮箱（选填）" />
        <a-input-password v-model:value="formPassword" placeholder="请输入密码（至少6位）" />
        <a-input-password v-model:value="formPasswordConfirm" placeholder="请再次输入密码" />
        <a-button type="primary" block :loading="loading" @click="handleRegister">
          注册
        </a-button>
      </a-space>
    </a-card>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { message } from 'ant-design-vue'
import { useUserStore } from '../store/user'
import { register } from '../api/auth'

const router = useRouter()
const userStore = useUserStore()

const formUsername = ref('')
const formEmail = ref('')
const formPassword = ref('')
const formPasswordConfirm = ref('')
const loading = ref(false)

const handleRegister = async () => {
  if (!formUsername.value || !formPassword.value || !formPasswordConfirm.value) {
    message.warning('请填写用户名和密码')
    return
  }
  if (formPassword.value !== formPasswordConfirm.value) {
    message.error('两次密码不一致')
    return
  }

  loading.value = true
  const data: any = {
    username: formUsername.value,
    password: formPassword.value,
    password_confirm: formPasswordConfirm.value,
  }
  if (formEmail.value) {
    data.email = formEmail.value
  }
  try {
    await register(data)
    message.success('注册成功！请登录')
    router.push('/login')
  } catch (err: any) {
    const errors = err.response?.data
    if (errors) {
      const errorArrays = Object.values(errors) as string[][]
      const msgs = errorArrays.reduce((acc: string[], val: string[]) => acc.concat(val), []).join('; ')
      message.error(msgs)
    } else {
      message.error('注册失败，请稍后重试')
    }
  } finally {
    loading.value = false
  }
}
</script>
