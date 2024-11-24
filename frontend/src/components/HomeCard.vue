<script setup>
import { ref } from 'vue'

const TestName = ref('')
const Address = ref('')
const getFile = ref(null)

const MoveOn = () => {
  console.log('Test Name:', TestName.value)
  console.log('Address:', Address.value)
  console.log('File:', getFile.value)
}

const handleFileChange = (event) => {
  getFile.value = event.target.files[0]
}
</script>

<template>
  <div class="container">
    <div class="tabs">
      <div class="tab">New</div>
      <div class="tab">History</div>
    </div>
    <h2>Create pentest</h2>
    <p>Create your penetration test in one click</p>
    <input 
      type="text" 
      v-model="TestName" 
      placeholder="Name of your test"
    />
    <input 
      type="url" 
      v-model="Address"
      placeholder="Host address"
    />
    <div>
      <input 
        type="file" 
        id="getFile" 
        @change="handleFileChange" 
        placeholder="vulnerability csv" 
        style="display: inline-block; width: 93%;" 
      />
    </div>
    <div class="button-row">
      <button id="deploy" @click="MoveOn">Deploy</button>
    </div>
  </div>
</template>