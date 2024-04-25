<template>
    <div class="m-2">
        <!-- 设置坐标 -->
        <div class="flex mt-4 w-full  align-items-center">
            <label class="w-6">最晚通知时间(单位:秒)</label>
            <input type="text" v-model="config.gather_notification_deadline"
                class="w-6 text-base text-color surface-overlay p-2 border-1 border-solid surface-border border-round appearance-none outline-none focus:border-primary"
                placeholder="检测周期(s)">
        </div>
        <div class="flex mt-4 w-full  align-items-center">
            <label class="w-6">通知时间频率(单位:秒)</label>
            <input type="text" v-model="config.gather_notification_interval"
                class="w-6 text-base text-color surface-overlay p-2 border-1 border-solid surface-border border-round appearance-none outline-none focus:border-primary"
                placeholder="检测周期(s)">
        </div>
        <div class="flex mt-4 w-full  align-items-center">
            <label class="w-6">检测频率(单位:秒)</label>
            <input type="text" v-model="config.gather_detection_interval"
                class="w-6 text-base text-color surface-overlay p-2 border-1 border-solid surface-border border-round appearance-none outline-none focus:border-primary"
                placeholder="检测周期(s)">
        </div>
        <div class="flex mt-4 w-full align-items-center">
            <label class="w-6">推送微信</label>
            <div class="flex flex-wrap gap-4">
                <div class="flex align-items-center">
                    <RadioButton v-model="config.gather_notification_enabled" :value="true" />
                    <label for="ingredient1" class="ml-2">开启</label>
                </div>
                <div class="flex align-items-center">
                    <RadioButton v-model="config.gather_notification_enabled" :value="false" />
                    <label for="ingredient2" class="ml-2">关闭</label>
                </div>
            </div>
        </div>
        <div class="flex mt-4 w-full  align-items-center">
            <label class="w-6">推送Token</label>
            <input type="text" v-model="config.gather_notification_token"
                class="w-6 text-base text-color surface-overlay p-2 border-1 border-solid surface-border border-round appearance-none outline-none focus:border-primary"
                placeholder="推送Token" :disabled="!config.gather_notification_enabled">
        </div>
        <div class="flex mt-4 w-full  align-items-center">
            <label class="w-6">推送对象</label>
            <div class="flex flex-wrap gap-4">
                <div class="flex align-items-center">
                    <RadioButton v-model="config.gather_notification_isGroup" :value="true" :disabled="!config.gather_notification_enabled"/>
                    <label for="ingredient1" class="ml-2">群聊</label>
                </div>
                <div class="flex align-items-center">
                    <RadioButton v-model="config.gather_notification_isGroup" :value="false" :disabled="!config.gather_notification_enabled" />
                    <label for="ingredient2" class="ml-2">个人</label>
                </div>
            </div>
        </div>
        <div class="flex mt-4 w-full  align-items-center">
            <label class="w-6">推送对象昵称</label>
            <input type="text" v-model="config.gather_notification_receiver"
                class="w-6 text-base text-color surface-overlay p-2 border-1 border-solid surface-border border-round appearance-none outline-none focus:border-primary"
                placeholder="推送对象昵称"  :disabled="!config.gather_notification_enabled">
        </div>
        <div class="w-full mt-4">
            <Button class="w-full justify-content-center" size="small" @click="saveConfig">
                <div>保存配置</div>
            </Button>
        </div>
        <Button class="w-full justify-content-center mt-4" size="small"
            @click="router.push({ path: '/' })">返回主菜单</Button>
        <Toast />
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import 'vue-advanced-cropper/dist/style.css';
import Toast from 'primevue/toast';
import { useToast } from 'primevue/usetoast';

const config = ref({
    gather_notification_deadline: 180,
    gather_notification_interval: 15,
    gather_detection_interval: 60,
    gather_notification_enabled: false,
    gather_notification_token: "dddd",
    gather_notification_receiver: "123",
    gather_notification_isGroup: false,
})
const toast = useToast();
const router = useRouter();

function getConfig() {
    fetch("http://localhost:8000/devices/config", {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
        },
    }).then((response) => {
        return response.json();
    }).then((data) => {
        if (data.data.gather_notification_deadline !== undefined) {
            config.value.gather_notification_deadline = data.data.gather_notification_deadline
        }
        if (data.data.gather_notification_interval !== undefined) {
            config.value.gather_notification_interval = data.data.gather_notification_interval
        }
        if (data.data.gather_detection_interval !== undefined) {
            config.value.gather_detection_interval = data.data.gather_detection_interval
        }
        if (data.data.gather_notification_enabled !== undefined) {
            config.value.gather_notification_enabled = data.data.gather_notification_enabled
        }
        if (data.data.gather_notification_token !== undefined) {
            config.value.gather_notification_token = data.data.gather_notification_token
        }
        if (data.data.gather_notification_receiver !== undefined) {
            config.value.gather_notification_receiver = data.data.gather_notification_receiver
        }
        if (data.data.gather_notification_isGroup !== undefined) {
            config.value.gather_notification_isGroup = data.data.gather_notification_isGroup
        }
    }).catch((error) => {
        toast.add({ severity: 'error', summary: '获取配置失败', detail: error.message, life: 3000 });
    });
}

function saveConfig() {
    fetch("http://localhost:8000/update/gather_config" ,{
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(config.value)
    }).then((response) => {
        return response.json();
    }).then((data) => {
        if (data.status_code === 200) {
            toast.add({ severity: 'success', summary: '保存配置成功', detail: data.message, life: 3000 });
        } else {
            toast.add({ severity: 'error', summary: '保存配置失败', detail: data.message, life: 3000 });
        }
    }).catch((error) => {
        toast.add({ severity: 'error', summary: '保存配置失败', detail: error.message, life: 3000 });
    });
}

onMounted(() => {
    getConfig()
})

</script>