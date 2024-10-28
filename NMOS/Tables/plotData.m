data = readtable("NMOS_Stack_11_W1.txt","FileType","text");
figure
t = tiledlayout(3,3);
nexttile
plot(data.V_drain1_,data.I_Vd_*1e9);
title("I(D1)")
ylabel("I(in nA)")
xlabel("Vdrain1 (in V)")
grid on
nexttile
plot(data.V_drain1_,data.I_Vd2_*1e9);
title("I(D2)")
ylabel("I(in nA)")
xlabel("Vdrain1 (in V)")
grid on
nexttile
plot(data.V_drain1_,data.I_Vb1_*1e9);
title("I(B1)")
ylabel("I(in nA)")
xlabel("Vdrain1 (in V)")
grid on
nexttile
plot(data.V_drain1_,data.I_Vb2_*1e9);
title("I(B2)")
ylabel("I(in nA)")
xlabel("Vdrain1 (in V)")
grid on
nexttile
plot(data.V_drain1_,data.I_Vg1_*1e9);
title("I(G1)")
ylabel("I(in nA)")
xlabel("Vdrain1 (in V)")
grid on
nexttile
plot(data.V_drain1_,data.I_Vg2_*1e9);
title("I(G2)")
ylabel("I(in nA)")
xlabel("Vdrain1 (in V)")
grid on
nexttile
plot(data.V_drain1_,data.V_net1_);
title("V(net1)")
ylabel("V(in V)")
xlabel("Vdrain1 (in V)")
grid on

title(t,"NMOS Stack 11")