<template>
  <main class="input-container">
    <center>
      <input
        type="text"
        name=""
        id="input"
        class="input"
        v-model="inputContent"
      />
      <br /><br />
      <h1>{{ inputContent }}</h1>
    </center>
  </main>
</template>

<script>
export default {
  name: "input",
  data: function () {
    return {
      inputContent: "",
    };
  },
  methods: {},
};
</script>

<style>
.input-container {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}

.input {
  color: black;
  font-size: 2rem;
  padding: 0.5rem 0.4rem;
}
</style>
