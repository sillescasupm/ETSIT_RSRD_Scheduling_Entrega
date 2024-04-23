class Zone:
    def __init__(self, name, users, bps_per_hz, r_peak_mbps, r_sla_mbps):
        self.name = name
        self.users = users
        self.bps_per_hz = bps_per_hz
        self.r_peak_mbps = r_peak_mbps
        self.r_sla_mbps = r_sla_mbps

    def __repr__(self):
        return f"Zone('{self.name}', {self.users}, {self.bps_per_hz}, {self.r_peak_mbps}, {self.r_sla_mbps})"

    def __lt__(self, other):
        return self.bps_per_hz > other.bps_per_hz
    
class Scenario:
    def __init__(self, b_total_MHz, zones):
        self.b_total_MHz = b_total_MHz
        self.b_remain_MHz = b_total_MHz
        self.zones = sorted(zones)
        print("Zones sorted by bps_per_hz:")
        for zone in self.zones:
            print(zone)


    def suma_valores(self, valores1, valores2):
        if len(valores1) != len(valores2):
            raise ValueError("Las listas deben tener la misma longitud")

        return [[v1[0], v1[1] + v2[1]] for v1, v2 in zip(valores1, valores2)]
        
    
    def computeZoneBps(self, zone):
        return zone.users * zone.bps_per_hz * self.b_total_MHz
    
    def computeZone(self, zone):
        n_users = zone.users
        ro_bpsHz = zone.bps_per_hz
        b_total = n_users * zone.r_peak_mbps / zone.bps_per_hz
        if b_total > self.b_remain_MHz:
            b_total = self.b_remain_MHz
        b_user = b_total / n_users
        r_user = b_user * ro_bpsHz
        return b_total, r_user
    
    def computeZoneMinSla(self, zone):
        n_users = zone.users
        ro_bpsHz = zone.bps_per_hz
        b_total = n_users * zone.r_sla_mbps / zone.bps_per_hz
        if b_total > self.b_remain_MHz:
            b_total = self.b_remain_MHz
        b_user = b_total / n_users
        r_user = b_user * ro_bpsHz
        return b_total, r_user

    def maxCI(self):
        r_final = []
        for zone in self.zones:
            zone_name = zone.name
            b_total, r_user = self.computeZone(zone)
            self.b_remain_MHz -= b_total
            r_final.append([zone_name, r_user])
        return r_final
    
    def maxCI_MinRate(self):
        r_final = []
        for zone in self.zones:
            zone_name = zone.name
            b_total, r_user = self.computeZoneMinSla(zone)
            self.b_remain_MHz -= b_total
            r_final.append([zone_name, r_user])
            zone.r_peak_mbps -= zone.r_sla_mbps

        r_final_maxCI = self.maxCI()

        result = self.suma_valores(r_final, r_final_maxCI)
        return result
    
    def proportionalFair(self):
        total_users = sum(zone.users for zone in self.zones)
        total_bandwidth = self.b_remain_MHz
        
        r_final = []
        for zone in self.zones:
            zone_name = zone.name
            fair_bandwidth = (zone.users / total_users) * total_bandwidth
            r_user = fair_bandwidth * zone.bps_per_hz / zone.users
            r_final.append([zone_name, r_user])
        self.b_remain_MHz = 0.0
        return r_final
    



    
def main():
    r_peak_mbps = 3
    r_sla_mbps = 0.3
    zones = [
        Zone("Z4", 14, 0.4, r_peak_mbps, r_sla_mbps),
        Zone("Z3", 19, 1.5, r_peak_mbps, r_sla_mbps),
        Zone("Z2", 9, 3, r_peak_mbps, r_sla_mbps),
        Zone("Z1", 8, 4.5, r_peak_mbps, r_sla_mbps),
    ]
    scenario = Scenario(25, zones)
    
    # Test maxCI
    r_final_maxCI = scenario.maxCI()
    print("\nResults for maxCI method:")
    for result in r_final_maxCI:
        print(f"Zone {result[0]}: {result[1]:.2f} Mbps/user")
    print(f"Remaining MHz after maxCI: {scenario.b_remain_MHz} MHz\n")

    # Reset scenario for the next method
    scenario.b_remain_MHz = scenario.b_total_MHz

    # Test maxCI_MinRate
    r_final_minRate = scenario.maxCI_MinRate()
    print("Results for maxCI_MinRate method:")
    for result in r_final_minRate:
        print(f"Zone {result[0]}: {float(result[1]):.2f} Mbps/user")
    print(f"Remaining MHz after maxCI_MinRate: {scenario.b_remain_MHz} MHz")

    # Reset scenario for the next method
    scenario.b_remain_MHz = scenario.b_total_MHz

    # Test proportionalFair
    r_final_proportional = scenario.proportionalFair()
    print("\nResults for proportionalFair method:")
    for result in r_final_proportional:
        print(f"Zone {result[0]}: {result[1]:.2f} Mbps/user")
    print(f"Remaining MHz after proportionalFair: {scenario.b_remain_MHz} MHz")

if __name__ == "__main__":
    main()
