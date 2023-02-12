<template>
  <form
    method="POST"
    @submit.prevent="submitQuery"
  >
    <div>
      <label for="product">Product</label>
      <select
        v-model="queryProduct"
        class="product"
        name="product"
      >
        <option
          v-for="(entry, index) in buildInfo"
          :key="index"
        >
          {{ entry.name }}
        </option>
      </select>
    </div>
    <div>
      <label for="branch">Branch</label>
      <select
        v-model="queryBranch"
        class="branch"
        name="branch"
      >
        <option
          v-for="(branch, index) in branches"
          :key="index"
        >
          {{ branch }}
        </option>
      </select>
    </div>
    <div>
      <label for="status">Status</label>
      <select
        v-model="queryStatus"
        class="status"
        name="status"
      >
        <option
          v-for="(status, index) in statuses"
          :key="index"
        >
          {{ status }}
        </option>
      </select>
    </div>
    <div>
      <label for="score">Score</label>
      <select
        v-model="queryScore"
        class="score"
        name="queryScore"
      >
        <option
          v-for="(score, index) in scores"
          :key="index"
        >
          {{ score }}
        </option>
      </select>
    </div>
    <div>
      <label for="date">Date</label>
      <input
        v-model="queryPriorDate"
        class="date"
        type="date"
        name="date"
      >
    </div>
    <div>
      <button
        type="button"
        @click="submitQuery"
      >
        Apply
      </button>
    </div>
  </form>
</template>

<script>
export default {
  data () {
    return {
      queryProduct: '',
      queryBranch: '',
      queryStatus: '',
      queryScore: '0',
      queryPriorDate: '',
      scores: ['0', '+1', '+2', '-1', '-2']
    }
  },
  computed: {
    isTestMode () {
      return this.$route.name.endsWith(':test')
    },
    buildInfo () {
      return this.$store.getters['manifestBrowser/buildInfo']
    },
    branches () {
      for (let entry of this.buildInfo) {
        if (entry.name === this.queryProduct) {
          return entry.branches
        }
      }
      return []
    },
    statuses () {
      for (let entry of this.buildInfo) {
        if (entry.name === this.queryProduct) {
          return entry['status']
        }
      }
      return []
    }
  },
  watch: {
    queryProduct () {
      if (!this.branches.includes(this.queryBranch)) {
        this.queryBranch = this.branches[0]
      }
      if (!this.statuses.includes(this.queryStatus)) {
        this.queryStatus = this.statuses[0]
      }
    }
  },
  created () {
    this.$store.dispatch('manifestBrowser/initializeFilter').then(() => {
      this.queryProduct = this.$store.getters['manifestBrowser/currentProduct']
      this.queryStatus = this.$store.getters['manifestBrowser/currentStatus']
      this.queryBranch = this.$store.getters['manifestBrowser/currentBranch']
      this.queryScore =
        this.$store.getters['manifestBrowser/currentVerificationStatus']
      this.queryScore = this.queryScore > 0
        ? '+' + this.queryScore.toString() : this.queryScore.toString()
      this.queryPriorDate =
        this.$store.getters['manifestBrowser/currentPriorDate']
      let queryResult = this.$store.getters['manifestBrowser/queryResult']
      if (queryResult.length === 0) {
        this.submitQuery()
      }
    })
  },
  methods: {
    submitQuery () {
      let filter = {}
      if (this.queryProduct !== 'all') {
        filter['product'] = this.queryProduct
      }
      if (this.queryBranch !== 'all') {
        filter['branch'] = this.queryBranch
      }
      if (this.queryStatus !== 'all') {
        filter['lifeCycleStatus'] = this.queryStatus
      }
      if (this.queryScore !== '0') {
        filter['verificationStatus'] = parseInt(this.queryScore)
      }
      if (this.queryPriorDate) {
        let timestamp = new Date(this.queryPriorDate)
        let hexSeconds = (86400 + Math.floor(timestamp / 1000)).toString(16)
        let constructedObjectId = hexSeconds + '0000000000000000'
        filter['id'] = { '$lte': constructedObjectId }
      }
      let queryForm = {
        'filter': filter,
        'date': this.queryPriorDate
      }
      this.$store.dispatch(
        'manifestBrowser/submitQuery',
        { 'payload': queryForm, 'isTestMode': this.isTestMode })
    }
  }
}
</script>

<style scoped lang="scss">
@import "@/styles/_variables.scss";
form {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  padding-top: 5px;
  padding-bottom: 3px;

  & .product, & .branch {
    width: 80px;
  }

  & .date {
    width: 120px;
  }

  & input[type=date]::-webkit-inner-spin-button,
  & input[type=date]::-webkit-outer-spin-button {
    -webkit-appearance: none;
  }

  & input, select {
    height: 20px;
    font-size: 13px;
    font-family: $font-stack-sans;
  }

  & label {
    margin-right: 5px;
  }

  & button {
    text-align: center;
    width: 50px;
  }

  & > div {
    margin: 0 10px;
  }
}
</style>
