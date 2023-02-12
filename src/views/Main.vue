<template>
  <div class="main">
    <div class="logo">
      <img
        src="@/assets/logo.svg"
        alt="app logo"
        style="width:80px"
      >
    </div>
    <div class="input">
      <input
        v-model="message"
        placeholder="enter at least two characters"
      >
    </div>
    <div class="result">
      <div
        class="entry"
        v-for="(item, index) in searchResult"
        :key="index"
      >
        <p class="person">{{ item.name }}</p>
        <div class="top">
          <p class="head">Films</p>
          <div
            class="subentry"
            v-for="(film, index2) in item.films"
            :key="index2"
          >
            <p class="subentry-head">{{ film }}</p>
          </div>
        </div>
        <div class="bottom">
          <p class="head">Vehicles</p>
          <div
            class="subentry"
            v-for="(vehicle, index3) in item.vehicles"
            :key="index3"
          >
            <p class="subentry-head">{{ vehicle }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { request, gql } from 'graphql-request'
const query = gql`
query MatchedPersons($text: String!) {
  searchText(text: $text)
  persons {
    name
    films
    vehicles
  }
}`
export default {
  data () {
    return {
      message: '',
      searchResult: []
    }
  },
  watch: {
    message (val, oldVal) {
      if (val.length < 2) {
        this.searchResult = []
        return
      }
      request({
        url: process.env.VUE_APP_BACKEND + '/myapp/graphql',
        document: query,
        variables: { text: this.message }
      }).then((data) => {
        if (data.errors) {
          console.log(data.errors)
        } else {
          this.searchResult = data.persons
        }
      }).catch(error => {
        console.log(error)
      })
    }
  }
}
</script>

<style lang="scss" scoped>
@import "@/styles/_variables.scss";
.main {
  & > .logo {
    width: 100%;
    height: 200px;
    padding-top: 110px;

    & img {
      display: block;
      margin-left: auto;
      margin-right: auto;
    }
  }
  & > .input {
    width: 100%;

    ::placeholder {
      font-size: 11pt;
    }

    & > input {
      display: block;
      font-size: 16pt;
      margin-left: auto;
      margin-right: auto;
    }
  }
  & > .result {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    margin-top: 20px;

    & > .entry {
      width: 220px;
      height: 300px;
      border-width: 1px;
      border-color: black;
      border-radius: 12px;
      background: #d9d3f2;

      &:hover {
        cursor: pointer;
      }

      & p.person {
        display: flex;
        align-items: center;
        justify-content: center;
        height: 30px;
        border-radius: 12px 12px 0 0;
        background: #5c337d;
        color: white;
      }

      & div.subentry {
        padding-left: 10px;
      }
      
      & div.top {
        height: 160px;
      }
      & p.head {
        margin: 10px 10px 0 10px;
        font-size: 10pt;
        font-weight: bold;
        height: 25px;
        border-width: 0 0 1px 0;
        border-style: solid;
        border-color: grey;
      }
      & p.subentry-head {
        font-size: 10pt;
        margin-bottom: 1pt;
      }
    }
  }
}
</style>
