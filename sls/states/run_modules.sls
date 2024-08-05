# run_modules:
#   module.run:
#     - name: sleeper.run


{% for i in range(3) %}
run_a_{{ i }}:
  module.run:
    - name: a.run
{% endfor %}