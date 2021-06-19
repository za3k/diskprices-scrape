summary.txt: index.html
	python parse.py index.html >$@
index.html:
	wget "https://diskprices.com/?locale=us&condition=new,used&disk_types=external_hdd,external_hdd25,internal_hdd,internal_hdd25,internal_sshd,internal_sas,external_ssd,internal_ssd,m2_ssd,m2_nvme,microsd,sd_card,cf_card,cfast_card,usb_flash,bdrw,bdr,dvdrw,dvdr,cdrw,cdr,lto3,lto4,lto5,lto6,lto7,lto8" -O $@ 
