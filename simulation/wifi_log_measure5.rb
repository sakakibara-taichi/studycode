#simply measure SSID and RSSI based on access point around you
#output to csv file 
#!/usr/local/bin/ruby

require 'csv'
require "fileutils"
require 'date'

# location of measuring
print "Continue? : "  
loc = gets
location = loc
loop{

    # set data variable 
    ssid = [] # SSID
    id = [0,0,0,0,0,0] # id of conneted AP 
    rssi = [0,0,0,0,0,0] # RSSI
    noise = [0,0,0,0,0,0] # Noise
    pass = [] # Password
    ipadress = [] # IPadress
    rate_max =[0,0,0,0,0,0] # Throughput 
    rate_lastTx = [0,0,0,0,0,0]
    throughput = [0,0,0,0,0,0]
    mcs = [0,0,0,0,0,0]
    channel = [0,0,0,0,0,0]
    day = [0,0,0,0,0,0]
    hour = [0,0,0,0,0,0]
    ap = []
    c_ap = []

    # want to measure ssid list
    CSV.foreach("ssid.csv") do |row|
        ssid.push(row[0])
    end

    system(" airport -I |grep 'AM' | awk '{print $0}' > id.txt")
    File.foreach('id.txt'){|line|
        ap = line.split(" ")
        c_ap = ap[1] + " " + ap[2] + " " +ap[3]
    }
    puts c_ap
    # one hop of connected AP
    for i in 0..5 do
        if ssid[i] == c_ap then
            id[i] = 1
        end
    end

    puts "success to measure ssid and rssi"
    #reading csv file
    # get password
    CSV.foreach("pass.csv") do |row|
        pass.push(row[0])
    end
    # get IPadress
    CSV.foreach("ipadress_false.csv") do |row|
        # p row[0]
        ipadress.push(row[0].to_i)
    end

    for k in 0..5 do
        puts "measure data of SSID : #{ssid[k]}"
        puts "switch AP : #{ssid[k]}"
        system("networksetup -setairportnetwork en0 '#{ssid[k]}' 4439944399") # switch access point 
        sleep 10
        
        # extract data of connected AP
        puts "execute airport -I !"
        system(" airport -I |grep -e 'CtlRSSI' -e 'CtlNoise' -e 'Rate' -e 'MCS' -e 'channel' -e 'AM' | awk '{print $0}' > AP.txt")
        File.foreach('AP.txt'){|line|
            newline = line.split(" ")
            if    /CtlRSSI/=~line then
                rssi[k] = newline[1].to_i
            elsif /CtlNoise/=~line then
                noise[k] = newline[1].to_i
            elsif /lastTxRate/=~line then
                rate_lastTx[k] = newline[1].to_i
            elsif /maxRate/=~line then
                rate_max[k] = newline[1].to_i
            elsif /MCS/=~line then
                mcs[k] = newline[1].to_i
            elsif /channel/=~line then
                channel[k] = newline[1].to_i
            end
            
        }
        
        # puts "execute iperf to server from client !"
        # system("iperf -c #{ipadress[4*k]}.#{ipadress[4*k+1]}.#{ipadress[4*k+2]}.#{ipadress[4*k+3]} > throughput.txt")
        # sleep 20 # sleep 20 seconds
        # #スループットだけ取り出す
        # puts "save iperf output"
        # File.foreach('throughput.txt'){|line|
        #     newline2 = line.split(" ") 
        #     if /sec/=~line then
        #         throughput[k] = newline2[6].to_i
        #         puts "save success"
        #     else
        #         puts "fill in zero"
        #         next
        #     end
        # }
        
    end
    # #saving total data 
    # puts "save data to csvfile"
    # puts "SSID"
    # puts ssid
    # puts "RSSI"
    # puts rssi
    # puts "AP ID"
    # puts id
    # puts "RATE"
    # # puts rate
    # puts "Throughput"
    # # puts throughput
    # puts "time"
    # puts time 
    time = DateTime.now.strftime('%m%d%H%M%S')
    # save csv file with location and date
    CSV.open("logdata/logdate_#{location}_#{time}.csv",'w') do |csv| # output to csv file
        csv << ["ssid"] + ssid
        csv << ["Cap"] +id
        csv << ["RSSI"] +rssi
        csv << ["Noise"] +noise
        csv << ["lastTxRate"] +rate_lastTx
        csv << ["maxRate"] +rate_max
        csv << ["mcs"] +mcs
        csv << ["channel"] +channel
        # csv << throughput
    end

    # decide to continue meausering
    print "Continue? : "  
    str = gets
    if str=="\n" then
    #     location += 1
        next
    else
        break
    end		
}