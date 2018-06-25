# this code is used to measure to access point log data
#!/usr/local/bin/ruby

require 'csv'
require "fileutils"

# ch = [36,40,48] #chanel decision
location = 1 # set to measurement position

loop{
	loop{
		print "Push (only) Enter Key when you are ready: " 
		str = gets
		if str=="\n" then
			break
		end
	}
	
	info=[] # for final data
	
	# for c in ch
	# 	system("sudo airport -z")
	# 	system("sudo airport -c#{c.to_s}")
		# system("sudo tcpdump -i en0 -tneI | grep 'Beacon' > tcpdump.txt & sleep 3") #command tcpdump for 3 seconds
        system("sudo tcpdump -i en0 -tneI > tcpdump.txt & sleep 3")
		system("sudo pkill tcpdump")# tcpdump停止


		data=[] # for saving confirm data
		temp=[] # for saving temporary data
		

		File.foreach('tcpdump.txt'){|line|  # reading each line
			unless /SA:/=~line then
				next
			end
			unless /dB/=~line then
				next
			end
            unless /Beacon/=~line then
				next
			end
			# deciding whether to exist in table
			catch :adding do
				for i in 0...temp.size 
                    if (line[(/SA:/=~line)+3,17]==temp[i][:macaddress])
                        # temp[i][:sample0] << line[(/sig/=~line)+1,(/6.0*/=~line)-3].to_i #SSIDと一致する場所から文字の位置を指定追加 
						temp[i][:sample1] << line[(/signal/=~line)-7,3].to_i # signalと一致する場所から7文字前を参照し追加 
						temp[i][:sample2] << line[(/noise/=~line)-8,4].to_i # noiseと一致する場所から7文字前を参照し追加 
						throw :adding
					end
				end
				# 新規登録
                temp[temp.size]={ :macaddress => line[(/SA:/=~line)+3,17], :SSID => line[(/Beacon/=~line)+8,15], :sample1 => [line[(/signal/=~line)-7,3].to_i], :sample2 => [line[(/noise/=~line)-8,4].to_i]
				}
			end
		}
		
		# average rssi and noise from sum data
		for i in 0...temp.size
			# temp[i][:rssi] = temp[i][:sample].max_by {|value| temp[i][:sample].count(value)}
			temp[i][:rssi]=temp[i][:sample1].inject(:+)/temp[i][:sample1].length  # rssiの平均
			temp[i][:noise]=temp[i][:sample2].inject(:+)/temp[i][:sample2].length # noiseの平均
			# if temp[i][:rssi] > -75 then
			data << [temp[i][:macaddress], temp[i][:SSID], temp[i][:rssi], temp[i][:noise], c]
            # end
            print data[i]
            puts "\n"
		end
        # print data
        puts "\n"
		info = info + data    
        FileUtils.cp("tcpdump.txt", "tcpdump#{c.to_s}.txt") 
        # system("tcpdump.txt > tcpdump#{c.to_s}.txt")
        system("rm tcpdump.txt")
	# end
	
	# output csv 
	CSV.open("data_location#{location.to_s}.csv",'w') do |csv|
			info.each do |bo|
				csv << bo
			end
	end
	
	print "Continue? : " 
	str = gets
	if str=="\n" then
		location += 1
		next
	else
		break
	end		
}

puts "END"