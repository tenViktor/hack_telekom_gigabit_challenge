<template>
  <div class="container">
    <div class="tabs">
      <div class="tab">New</div>
      <div class="tab">History</div>
    </div>
    <h2>Create pentest</h2>
    <p>Create your penetration test in one click</p>
    <input type="text" placeholder="Name of your test" />
    <select>
      <option>Select</option>
    </select>
    <div class="button-row">
      <button>Cancel</button>
      <button id="deploy">Deploy</button>
    </div>
  </div>
</template>

<script setup>
// You can add Vue reactive states, methods, or imports here as needed
</script>

<style scoped>
body {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  margin: 0;
  background-color: #f5f5f7;
}

.container {
  text-align: center;
  background-color: white;
  padding: 2em;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  width: 300px;
}

.tabs {
  display: flex;
  justify-content: center;
  margin-bottom: 20px;
}

.tab {
  padding: 10px 20px;
  background-color: #f1f3f5;
  border-radius: 5px;
  margin-right: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.tab:hover {
  background-color: #e0e0e0;
}

#deploy {
  background-color: #d63384;
  color: white;
  border: none;
  border-radius: 5px;
  padding: 10px;
  cursor: pointer;
  transition: background-color 0.3s;
}

#deploy:hover {
  background-color: #c2185b;
}

input,
select {
  width: 100%;
  padding: 10px;
  margin: 10px 0;
  border-radius: 5px;
  border: 1px solid #ccc;
}

.button-row {
  display: flex;
  justify-content: space-between;
}

.button-row button {
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
}

.button-row button:first-child {
  background-color: white;
}
</style>