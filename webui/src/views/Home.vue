<template>
    <div class="h-full flex flex-column bg-gray-300">
        <div class="h-12rem p-3 bg-primary border-round m-2 ">
            <div class="flex align-items-center">
                <label style="width:100px">当前设备</label>
                <div class="flex align-items-center">
                    <div>{{ deviceInfo.deviceName }}</div>
                </div>
            </div>
            <div class="flex align-items-center mt-2">
                <label style="width:100px">链接地址</label>
                <div class="flex align-items-center">{{ deviceInfo.deviceID }}</div>
            </div>
            <div class="flex align-items-center mt-2">
                <label style="width:100px">运行状态</label>
                <div class="flex align-items-center"><span>{{ deviceInfo.deviceStatus ? '在线' : '离线' }}</span></div>
            </div>
            <div class="flex mt-2">
                <Button class="w-full justify-content-center" @click="newDivceDialogVisible = true">
                    <div><i class="pi pi-plus mr-2"></i>新增设备</div>
                </Button>
                <Button class="w-full justify-content-center" @click="openDeviceManageDialog">
                    <div><i class="pi pi-arrow-right-arrow-left mr-2"></i>设备管理</div>
                </Button>

            </div>

        </div>
        <div class="h-full m-2">
            <div class="flex bg-primary w-full border-round  align-items-center h-4rem">
                <div id="icon" class="flex  h-full  w-4rem align-items-center justify-content-center"><i
                        class="pi pi-th-large" style="font-size: 1.5rem;"></i></div>
                <div class="w-full h-full  flex justify-content-between align-items-center">
                    <div class="ml-2">测试功能一</div>
                    <div class="flex">
                        <Button>配置</Button>
                        <Button>启用</Button>
                    </div>
                </div>

            </div>
            <div class="flex  bg-primary w-full border-round  align-items-center h-4rem mt-2">
                <div id="icon" class="flex  h-full  w-4rem align-items-center justify-content-center"><i
                        class="pi pi-th-large" style="font-size: 1.5rem;"></i></div>
                <div class="w-full h-full  flex justify-content-between align-items-center">
                    <div class="ml-2">测试功能二</div>
                    <div class="flex">
                        <Button>配置</Button>
                        <Button>启用</Button>
                    </div>
                </div>

            </div>
        </div>
    </div>

    <!-- 新增设备弹窗 -->
    <Dialog v-model:visible="newDivceDialogVisible" modal header="新增设备" :style="{ width: '25rem' }">
        <span class="p-text-secondary block mb-5">新增设备连接</span>
        <div class="flex align-items-center gap-3 mb-3">
            <label for="username" class="font-semibold w-6rem">设备名称</label>
            <InputText id="username" class="flex-auto" autocomplete="off" v-model="deviceInfo.deviceName" />
        </div>
        <div class="flex align-items-center gap-3 mb-5">
            <label for="email" class="font-semibold w-6rem">链接地址</label>
            <InputText id="email" class="flex-auto" autocomplete="off" v-model="deviceInfo.deviceID" />
        </div>
        <div class="flex justify-content-end gap-2">
            <Button type="button" label="取消" severity="secondary" @click="newDivceDialogVisible = false"></Button>
            <Button type="button" label="测试" severity="info" @click="newDivceDialogVisible = false"></Button>
            <Button type="button" label="保存" @click="addDevice"></Button>
        </div>
    </Dialog>

    <!-- 切换设备弹窗 -->
    <Dialog v-model:visible="deviceManageDialogVisible" header="设备管理" :style="{ width: '25rem' }">
        <div class="w-full">
            <Dropdown class="w-full" v-model="selectedDevice" :options="deviceList" optionLabel="device_name"
                placeholder="选择设备" @select="handleSelect">
                <template #option="slotProps">
                    <div class="flex w-full justify-content-between align-items-center ">
                        <div>{{ slotProps.option.device_name }}</div>
                        <div class="text-sm ml-2 text-gray-400">{{ slotProps.option.device_id }}</div>
                    </div>
                </template>
            </Dropdown>
        </div>
        <div class="flex justify-content-end gap-2 mt-5">
            <Button type="button" label="删除设备" severity="danger" @click="deleteDevice"></Button>
            <Button type="button" label="切换设备" @click="switchDevice"></Button>
        </div>

    </Dialog>
    <Toast />
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useToast } from 'primevue/usetoast';
import Toast from 'primevue/toast';

const toast = useToast();
const deviceInfo = ref({
    deviceName: '',
    deviceID: '',
    deviceStatus: false,
});
const selectedDevice = ref({});
const deviceList = ref([]);
const newDivceDialogVisible = ref(false);
const deviceManageDialogVisible = ref(false);

function handleSelect({ originalEvent, value }) {
    console.log("selected originalEvent: ", originalEvent);
    console.log("selected value: ", value);
}

// 添加设备
function addDevice() {
    fetch('http://127.0.0.1:8000/devices/add', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ device_id: deviceInfo.value.deviceID, device_name: deviceInfo.value.deviceName })
    })
        .then(response => response.json())
        .then(data => {
            if (data.status_code !== undefined && data.status_code === 200) {
                toast.add({ severity: 'success', summary: '设备添加成功', detail: data.message, life: 3000 });
            } else {
                toast.add({ severity: 'error', summary: '设备添加失败', detail: data.message, life: 3000 });
            }
        })
        .catch((error) => {
            toast.add({ severity: 'error', summary: '设备添加失败', detail: error, life: 3000 });
        });
    newDivceDialogVisible.value = false;
}


// 管理设备
function openDeviceManageDialog() {
    fetch('http://127.0.0.1:8000/devices/list')
        .then(response => response.json())
        .then(data => {
            if (data.status_code !== undefined && data.status_code === 200) {
                console.log(data)
                deviceList.value = data.data;
            } else {
                toast.add({ severity: 'error', summary: '设备列表获取失败', detail: data.message, life: 3000 });
            }
        })
        .catch((error) => {
            toast.add({ severity: 'error', summary: '设备列表获取失败', detail: error, life: 3000 });
        });
    deviceManageDialogVisible.value = true;
}

// 切换设备
function switchDevice() {
    console.log("selected device: ", selectedDevice.value);

    // fecth get 请求，请求参数为device_name
    fetch('http://127.0.0.1:8000/devices/switch?device_name=' + selectedDevice.value.device_name, {
        method: 'GET',
    })
        .then(response => response.json())
        .then(data => {
            if (data.status_code !== undefined && data.status_code === 200) {
                refreshDeviceInfo()
                toast.add({ severity: 'success', summary: '设备切换成功', detail: data.message, life: 3000 });
                deviceManageDialogVisible.value = false;
            } else {
                toast.add({ severity: 'error', summary: '设备切换失败', detail: data.message, life: 3000 });
            }
        })
        .catch((error) => {
            toast.add({ severity: 'error', summary: '设备切换失败', detail: error, life: 3000 });
        });
}

// 删除设备
function deleteDevice() {
    console.log("selected device: ", selectedDevice.value);

    // fecth delete 请求，请求参数为device_name
    fetch('http://127.0.0.1:8000/devices/delete?device_name=' + selectedDevice.value.device_name, {
        method: 'DELETE',
    })
        .then(response => response.json())
        .then(data => {
            if (data.status_code !== undefined && data.status_code === 200) {
                toast.add({ severity: 'success', summary: '设备删除成功', detail: data.message, life: 3000 });
                deviceList.value = deviceList.value.filter(item => item.device_name !== selectedDevice.value.device_name);
                deviceManageDialogVisible.value = false;
            } else {
                toast.add({ severity: 'error', summary: '设备删除失败', detail: data.message, life: 3000 });
            }
        })
        .catch((error) => {
            toast.add({ severity: 'error', summary: '设备删除失败', detail: error, life: 3000 });
        });
}

function refreshDeviceInfo() {
    fetch('http://127.0.0.1:8000/devices/current')
        .then(response => response.json())
        .then(data => {
            if (data.status_code !== undefined && data.status_code === 200) {
                deviceInfo.value.deviceName = data.data.device_name;
                deviceInfo.value.deviceID = data.data.device_id;
                deviceInfo.value.deviceStatus = data.data.device_status;
            } else {
                toast.add({ severity: 'error', summary: '设备信息获取失败', detail: data.message, life: 3000 });
            }
        })
        .catch((error) => {
            toast.add({ severity: 'error', summary: '设备信息获取失败', detail: error, life: 3000 });
        });
}

onMounted(() => {
    refreshDeviceInfo()
})

</script>



<style scoped></style>