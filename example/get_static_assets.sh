verify_checksum(){
	if [[ -f "$1" ]]
		then
			cs="$(shasum -b -a 256 "$1" | awk '{ print $1 }' | xxd -r -p | base64)"
			valid_cs="$(grep -c "$2" <<<"$cs")"
			echo $cs
			echo $valid_cs
			if [[ $valid_cs -eq 1 ]]
				then
					echo ok
				else	
					echo check file 
			fi

	fi		
}
	


sudo apt install -y wget
wget https://code.jquery.com/jquery-1.12.4.min.js
wget https://cdnjs.cloudflare.com/ajax/libs/socket.io/2.2.0/socket.io.js

verify_checksum jquery-1.12.4.min.js "ZosEbRLbNQzLpnKIkEdrPv7lOy9C27hHQ+Xp8a4MxAQ="
verify_checksum socket.io.js "yr4fRk/GU1ehYJPAs8P4JlTgu0Hdsp4ZKrx8bDEDC3I="

mv jquery-1.12.4.min.js static/
mv socket.io.js static/
	
