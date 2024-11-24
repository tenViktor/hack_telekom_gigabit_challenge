<script setup>
import { ref } from 'vue'

const TestName = ref('')
const Address = ref('')
const getFile = ref(null)

const MoveOn = () => {
  console.log('Test Name:', TestName.value)
  console.log('Address:', Address.value)
  console.log('File:', getFile.value ? getFile.value.name : 'No file selected')
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
    <h2>Create Pentest</h2>
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

    <!-- Display User Inputs -->
<!--    <div style="margin-top: 20px;">
      <h3>Preview Input:</h3>
      <p><strong>Test Name:</strong> {{ TestName }}</p>
      <p><strong>Host Address:</strong> {{ Address }}</p>
      <p><strong>Selected File:</strong> {{ getFile ? getFile.name : 'No file selected' }}</p>
    </div>
  </div>
</template> -->
