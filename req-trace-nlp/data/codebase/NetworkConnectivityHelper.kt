class NetworkConnectivityHelper {
    fun isOnline(activeTransportWifi: Boolean, activeTransportCellular: Boolean): Boolean {
        return activeTransportWifi || activeTransportCellular
    }
}
