run_state:
  salt.state:
    - tgt: '*'
    - sls:
      - sls/states/run_modules
    - batch: 30
    - timeout: 120
