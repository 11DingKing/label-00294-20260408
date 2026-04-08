<template>
  <el-container class="layout-container">
    <el-aside width="240px" class="aside">
      <div class="aside-header">
        <div class="logo-wrapper">
          <div class="logo-icon">
            <el-icon :size="24"><ShoppingBag /></el-icon>
          </div>
          <span class="logo-text">订单管理</span>
        </div>
      </div>

      <el-menu :default-active="activeMenu" router class="aside-menu">
        <el-menu-item index="/orders">
          <el-icon><Document /></el-icon>
          <template #title>订单管理</template>
        </el-menu-item>
        <el-menu-item index="/statistics">
          <el-icon><DataAnalysis /></el-icon>
          <template #title>数据统计</template>
        </el-menu-item>
      </el-menu>
    </el-aside>

    <el-container class="main-container">
      <el-header class="header">
        <div class="header-left">
          <h2 class="page-title">{{ pageTitle }}</h2>
        </div>
        <div class="header-right">
          <el-dropdown @command="handleCommand" trigger="click">
            <div class="user-dropdown">
              <el-avatar :size="36" class="user-avatar">
                {{ authStore.username?.charAt(0)?.toUpperCase() }}
              </el-avatar>
              <div class="user-info">
                <span class="user-name">{{ authStore.username }}</span>
                <span class="user-role">管理员</span>
              </div>
              <el-icon class="dropdown-arrow"><ArrowDown /></el-icon>
            </div>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="changePassword">
                  <el-icon><Key /></el-icon>
                  修改密码
                </el-dropdown-item>
                <el-dropdown-item command="logout" divided>
                  <el-icon><SwitchButton /></el-icon>
                  退出登录
                </el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </el-header>

      <el-main class="main">
        <router-view v-slot="{ Component }">
          <transition name="page" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </el-main>
    </el-container>

    <!-- 修改密码对话框 -->
    <el-dialog
      v-model="showPasswordDialog"
      title="修改密码"
      width="420px"
      :close-on-click-modal="false"
    >
      <el-form
        ref="passwordFormRef"
        :model="passwordForm"
        :rules="passwordRules"
        label-position="top"
      >
        <el-form-item label="当前密码" prop="oldPassword">
          <el-input
            v-model="passwordForm.oldPassword"
            type="password"
            show-password
            placeholder="请输入当前密码"
            size="large"
          />
        </el-form-item>
        <el-form-item label="新密码" prop="newPassword">
          <el-input
            v-model="passwordForm.newPassword"
            type="password"
            show-password
            placeholder="请输入新密码（至少6位）"
            size="large"
          />
        </el-form-item>
        <el-form-item label="确认新密码" prop="confirmPassword">
          <el-input
            v-model="passwordForm.confirmPassword"
            type="password"
            show-password
            placeholder="请再次输入新密码"
            size="large"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showPasswordDialog = false" size="large"
          >取消</el-button
        >
        <el-button
          type="primary"
          :loading="passwordLoading"
          @click="handleChangePassword"
          size="large"
        >
          确认修改
        </el-button>
      </template>
    </el-dialog>
  </el-container>
</template>

<script setup>
import { computed, ref, reactive } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useAuthStore } from "@/store/auth";
import { ElMessageBox } from "element-plus";
import { toast, notify } from "@/utils/toast";
import {
  Document,
  ShoppingBag,
  ArrowDown,
  SwitchButton,
  Key,
  DataAnalysis,
} from "@element-plus/icons-vue";

const route = useRoute();
const router = useRouter();
const authStore = useAuthStore();

const activeMenu = computed(() => route.path);

const pageTitle = computed(() => {
  const titles = {
    "/orders": "订单管理",
    "/orders/create": "新建订单",
    "/statistics": "数据统计",
  };
  if (route.path.match(/^\/orders\/\d+$/)) {
    return "订单详情";
  }
  return titles[route.path] || "订单管理";
});

// 修改密码
const showPasswordDialog = ref(false);
const passwordLoading = ref(false);
const passwordFormRef = ref(null);
const passwordForm = reactive({
  oldPassword: "",
  newPassword: "",
  confirmPassword: "",
});

const validateConfirmPassword = (rule, value, callback) => {
  if (value !== passwordForm.newPassword) {
    callback(new Error("两次输入的密码不一致"));
  } else {
    callback();
  }
};

const passwordRules = {
  oldPassword: [{ required: true, message: "请输入当前密码", trigger: "blur" }],
  newPassword: [
    { required: true, message: "请输入新密码", trigger: "blur" },
    { min: 6, message: "密码长度不能少于6位", trigger: "blur" },
  ],
  confirmPassword: [
    { required: true, message: "请再次输入新密码", trigger: "blur" },
    { validator: validateConfirmPassword, trigger: "blur" },
  ],
};

const handleChangePassword = async () => {
  if (!passwordFormRef.value) return;

  await passwordFormRef.value.validate(async (valid) => {
    if (valid) {
      passwordLoading.value = true;
      try {
        const success = await authStore.changePassword(
          passwordForm.oldPassword,
          passwordForm.newPassword,
        );
        if (success) {
          showPasswordDialog.value = false;
          passwordForm.oldPassword = "";
          passwordForm.newPassword = "";
          passwordForm.confirmPassword = "";
          notify.success("修改成功", "密码已更新，请使用新密码登录");
        }
      } finally {
        passwordLoading.value = false;
      }
    }
  });
};

const handleCommand = async (command) => {
  if (command === "logout") {
    try {
      await ElMessageBox.confirm("确定要退出登录吗？", "退出确认", {
        confirmButtonText: "确定退出",
        cancelButtonText: "取消",
        type: "warning",
      });
      await authStore.logout();
      toast.success("已安全退出");
      router.push("/login");
    } catch (error) {
      // 用户取消
    }
  } else if (command === "changePassword") {
    showPasswordDialog.value = true;
  }
};
</script>

<style scoped lang="scss">
.layout-container {
  height: 100vh;
  background: #f3f4f6;
}

.aside {
  background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%);
  display: flex;
  flex-direction: column;
  box-shadow: 4px 0 24px rgba(0, 0, 0, 0.1);
}

.aside-header {
  padding: 20px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);

  .logo-wrapper {
    display: flex;
    align-items: center;
    gap: 12px;

    .logo-icon {
      width: 40px;
      height: 40px;
      background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
      border-radius: 10px;
      display: flex;
      align-items: center;
      justify-content: center;
      color: white;
      flex-shrink: 0;
    }

    .logo-text {
      color: white;
      font-size: 18px;
      font-weight: 700;
      white-space: nowrap;
    }
  }
}

.aside-menu {
  flex: 1;
  border: none;
  background: transparent;
  padding: 12px 8px;

  :deep(.el-menu-item) {
    height: 48px;
    line-height: 48px;
    margin: 4px 0;
    border-radius: 10px;
    color: rgba(255, 255, 255, 0.7);
    transition: all 0.2s ease;

    &:hover {
      background: rgba(255, 255, 255, 0.1);
      color: white;
    }

    &.is-active {
      background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
      color: white;
      box-shadow: 0 4px 12px rgba(99, 102, 241, 0.4);
    }

    .el-icon {
      font-size: 20px;
    }
  }
}

.main-container {
  flex-direction: column;
}

.header {
  background: white;
  height: 72px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 28px;
  border-bottom: 1px solid #e5e7eb;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);

  .page-title {
    font-size: 22px;
    font-weight: 700;
    color: #1f2937;
    margin: 0;
  }
}

.user-dropdown {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px 12px;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.2s ease;

  &:hover {
    background: #f3f4f6;
  }

  .user-avatar {
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
    color: white;
    font-weight: 600;
  }

  .user-info {
    display: flex;
    flex-direction: column;

    .user-name {
      font-size: 14px;
      font-weight: 600;
      color: #1f2937;
      line-height: 1.2;
    }

    .user-role {
      font-size: 12px;
      color: #6b7280;
    }
  }

  .dropdown-arrow {
    color: #9ca3af;
    font-size: 12px;
  }
}

.main {
  padding: 0;
  overflow-y: auto;
  background: #f3f4f6;
}

// 页面切换动画
.page-enter-active,
.page-leave-active {
  transition:
    opacity 0.25s ease,
    transform 0.25s ease;
}

.page-enter-from {
  opacity: 0;
  transform: translateX(20px);
}

.page-leave-to {
  opacity: 0;
  transform: translateX(-20px);
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
