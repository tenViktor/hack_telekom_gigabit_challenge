  <!-- src/App.vue -->

<script> 
  export default {
    data() {
      return 
    }
  }
</script>
  <template>
    <title>Create Pentest</title>
    <div class="container">
        <div class="tabs">
            <div class="tab">New</div>
            <div class="tab">History</div>
        </div>
        <h2>Create pentest</h2>
        <p>Create your penetration test in one click</p>
        <input type="text" id=TestName placeholder="Name of your test" width="100px" />
        <input type="url" id=Address  placeholder="host address" width="100px" />
        <div>
        <label for="getFile" class="btn">Vulnerability CSV</label>
        <input type="file" id=getFile placeholder="vulnerability csv" style="display: Vuln" width="100px" />
        <div class= "button-row">
            <button id="deploy">Deploy</button>
        </div>
    </div>
    </div>

  </template>

  <style>
  /* Any global styles */
  </style>