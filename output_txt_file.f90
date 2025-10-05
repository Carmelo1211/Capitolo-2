subroutine write_txt_file(k_file,traslay)
 use Variabili
 implicit none

 character(80):: datafile_tec,kcar
 integer :: i,j,k_file,m,p
 real(4):: traslay


 if(k_file.lt.10) then
	write(kcar,'(i1)') k_file
	else if(k_file.lt.100) then
	write(kcar,'(i2)') k_file
	else if(k_file.lt.1000) then
	write(kcar,'(i3)') k_file
	else if(k_file.lt.10000) then
	write(kcar,'(i4)') k_file
	else if(k_file.lt.100000) then
	write(kcar,'(i5)') k_file
	else if(k_file.lt.1000000) then
	write(kcar,'(i6)') k_file
	else if(k_file.lt.10000000) then
	write(kcar,'(i7)') k_file
	else if(k_file.lt.100000000) then
	write(kcar,'(i8)') k_file
	else if(k_file.lt.1000000000) then
	write(kcar,'(i9)') k_file
	end if


 datafile_tec=kcar(1:index(kcar,' ')-1)//'.txt'


 open(unit=1, file=datafile_tec)

 write(1,*) "[Valori_Elementi]"
 write(1,*) "x_c y_c rho_c P_c u_c v_c M S"
 write(1,*)
 do i=1,nele_interni
    write(1,*) ele(i)%x0(1), ele(i)%x0(2), ele(i)%ucons(2), ele(i)%P, ele(i)%u, ele(i)%v, sqrt(ele(i)%u**2+ele(i)%v**2)/ele(i)%a, ele(i)%S
 end do

write(1,*)
write(1,*) "[Nodi]"
write(1,*) "Elementi condivisi dal nodo"," x", " y"
write(1,*)

m=maxval(nodo(:)%neles)
do i=1,nnodi
    j=1
    p=1
    do while (j.le.nodo(i)%neles)
        write(1,'(I0,1X)',ADVANCE="NO") nodo(i)%ele(j)
        j=j+1
    end do

    if (nodo(i)%neles.lt.m) then
        do while (p.le.m-nodo(i)%neles)
            write(1,'(I0,1X)',ADVANCE="NO") 0
            p=p+1
        end do
    end if


    write(1,*) nodo(i)%x(1),nodo(i)%x(2)

 end do



end subroutine
