# codemposer
Compose music from any of your code files.

A continuation of [SourceCodeSonificator](https://github.com/YilunAllenChen/SourceCodeSonificator)

# Sonic-pi
You need this snippet running on sonic pi.
```ruby
live_loop :foo do
  use_real_time
  cmds = sync "/osc*/run-code"
  run_code cmds[1]
end
```
