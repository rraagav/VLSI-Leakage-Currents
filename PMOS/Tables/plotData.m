data = readtable("PMOS_Stack_11_W1.txt","FileType","text");
figure
t = tiledlayout(3,3);
nexttile
plot(data.V_source1_,data.I_Vs1_*1e9);
title("I(S1)")
ylabel("I(in nA)")
xlabel("Vsource1 (in V)")
grid on
nexttile
plot(data.V_source1_,data.I_Vg1_*1e9);
title("I(G1)")
ylabel("I(in nA)")
xlabel("Vsource1 (in V)")
grid on
nexttile
plot(data.V_source1_,data.I_Vnet_*1e9);
title("I(D1)")
ylabel("I(in nA)")
xlabel("Vsource1 (in V)")
grid on
nexttile
plot(data.V_source1_,data.I_Vb1_*1e9);
title("I(B1)")
ylabel("I(in nA)")
xlabel("Vsource1 (in V)")
grid on
nexttile
plot(data.V_source1_,data.I_Vg2_*1e9);
title("I(G2)")
ylabel("I(in nA)")
xlabel("Vsource1 (in V)")
grid on
nexttile
plot(data.V_source1_,data.I_Vd2_*1e9);
title("I(D2)")
ylabel("I(in nA)")
xlabel("Vsource1 (in V)")
grid on
nexttile
plot(data.V_source1_,data.I_Vb2_*1e9);
title("I(B2)")
ylabel("I(in nA)")
xlabel("Vsource1 (in V)")
grid on
nexttile
plot(data.V_source1_,data.V_drain1_);
grid on
title("Vd1")
ylabel("V(in V)")
xlabel("Vsource1 (in V)")

title(t,"PMOS Stack 11")