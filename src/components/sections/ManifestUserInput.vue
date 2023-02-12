<template>
  <div
    v-if="isVisible"
    class="root"
  >
    <div class="title-select">
      <span>&#9758;</span>
      <select v-model="selectedTitle">
        <option
          value=""
          disabled
        >
          Select from the following flags
        </option>
        <option
          v-for="(entry, index) in availableFlagSelections"
          :key="index"
        >
          {{ entry.subject }}
        </option>
      </select>
    </div>
    <textarea
      v-model="message"
      placeholder="Put description here"
    />
    <div class="bottom-ui">
      <p class="score-head">
        Score
      </p>
      <ul>
        <li
          v-for="(score, index) in availableScoreSelections"
          :key="index"
        >
          <div>{{ score.label }}</div>
          <div>
            <input
              v-model="scoreIndex"
              type="radio"
              :value="index"
            >
          </div>
        </li>
      </ul>
      <p class="score-description">
        {{ availableScoreSelections[scoreIndex].description }}
      </p>
    </div>
    <div class="buttons">
      <p class="error-message">
        {{ errorMessage }}
      </p>
      <button
        class="button-post"
        @click="postEntry"
      >
        Post
      </button>
      <button
        class="button-cancel"
        @click="$emit('hideUserInput')"
      >
        Cancel
      </button>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    show: Boolean
  },
  data () {
    return {
      isVisible: false,
      scoreIndex: 2,
      selectedTitle: '',
      message: '',
      errorMessage: ''
    }
  },
  computed: {
    isTestMode () {
      return this.$route.name.endsWith(':test')
    },
    availableFlagSelections () {
      return this.$store.getters['userGroupInfo']['deliveryFlags']
    },
    availableScoreSelections () {
      return [
        {
          label: '-2',
          value: -2,
          description: 'Let\'s discard this build'
        },
        {
          label: '-1',
          value: -1,
          description: 'I would prefer to discard this build'
        },
        {
          label: '+1',
          value: 1,
          description: 'Looks good, but someone else must approve'
        },
        {
          label: '+2',
          value: 2,
          description: 'Looks good to me, approved'
        }
      ]
    },
    appUser () {
      return this.$store.getters['appUser']
    }
  },
  watch: {
    show (value) {
      this.errorMessage = ''
      this.isVisible = value
    }
  },
  methods: {
    postEntry () {
      if (!this.selectedTitle) {
        this.errorMessage = 'Select a subject'
        return
      }
      if (!this.message || this.message.length < 30) {
        this.errorMessage = 'Length is not long enough'
        return
      }
      const entry = {
        user: {
          displayName: this.appUser.displayName,
          email: this.appUser.email
        },
        score: this.availableScoreSelections[this.scoreIndex].value,
        subject: this.selectedTitle,
        body: this.message,
        timestamp: new Date().toISOString()
      }
      this.$store.dispatch(
        'manifestBrowser/postNewUserEntry',
        { 'entry': entry, 'isTestMode': this.isTestMode })
      this.$emit('hideUserInput')
    }
  }
}
</script>

<style lang="scss" scoped>
@import "@/styles/_variables.scss";

div.root {
  background: lightgrey;
  padding: 5px 5px 10px 5px;
}

div.title-select {
  & > span {
    position: relative;
    bottom: -2px;
    margin-right: 5px;
    font-size: 24px;
  }
  & > select {
    margin: 10px 0 10px 0;
    width: 400px;
  }
}

textarea {
  min-width: 500px;
  min-height: 200px;
  padding: 5px;
  border: solid 1px #0099ff;
}

div.bottom-ui {
  display:flex;
  align-items: flex-end;
  font-size: 13px;
  width: 100%;

  & > ul {
    display:flex;
    position: relative;
    top: 3px;

    & > li {
      width: 20px;
      margin: 0 5px 0 10px;

      & > div {
        text-align: right;
      }
    }
  }

  & > p.score-description {
    font-size: 12px;
    margin-left: 12px;
  }
}

div.buttons {
  display:flex;
  margin-top: 10px;
  padding-top: 10px;
  border-top: solid 1px #999;

  & > button {
    width: 80px;
    text-align: center;
    height: 20px;
    font-size: 12px;
    box-shadow: none;
    margin-right: 10px;

    &.button-post {
      margin-left: auto;
      background: #0099ff;
      color: white;
      font-weight: bold;
    }
  }

  & > p.error-message {
    height: 15px;
    color: red;
    margin: 0 20px 7px 0;
    font-size: 12px;
    text-align: right;
  }
}
</style>
