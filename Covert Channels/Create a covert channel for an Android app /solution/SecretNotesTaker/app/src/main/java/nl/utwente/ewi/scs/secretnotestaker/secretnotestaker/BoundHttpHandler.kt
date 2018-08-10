package nl.utwente.ewi.scs.secretnotestaker.secretnotestaker

import java.net.InetAddress
import java.net.InetSocketAddress
import java.net.Socket
import java.net.ServerSocket
import java.net.SocketException
import java.net.UnknownHostException
import javax.net.SocketFactory

import java.io.IOException
import java.net.Proxy
import java.net.ResponseCache
import java.net.URL
import java.net.URLConnection
import java.net.URLStreamHandler
import java.util.BitSet

import android.util.Log

import okhttp3.OkHttpClient
import okhttp3.OkUrlFactory

class BoundSocketFactory(val localPort : Int) : SocketFactory() {
    override fun createSocket() : Socket {
        return addSocketOptions(Socket())
    }

    override fun createSocket(host : String, port : Int) : Socket {
        return addSocketOptions(Socket(host, port))
    }

    override fun createSocket(address : InetAddress, port : Int) : Socket {
        return addSocketOptions(Socket(address, port))
    }

    override fun createSocket(host : String, port : Int, clientAddress : InetAddress, clientPort : Int) : Socket {
        return addSocketOptions(Socket(host, port, clientAddress, clientPort))
    }

    override fun createSocket(address : InetAddress, port : Int, clientAddress : InetAddress, clientPort : Int) : Socket {
        return addSocketOptions(Socket(address, port, clientAddress, clientPort))
    }

    fun addSocketOptions(socket : Socket) : Socket {
        socket.bind(InetSocketAddress(localPort));

        return socket
    }
}

class BoundHttpHandler(val localPort : Int) : URLStreamHandler() {
    override fun openConnection(url : URL) : URLConnection {
        val client = OkHttpClient.Builder()
            .socketFactory(BoundSocketFactory(localPort))
            .build()

        return OkUrlFactory(client).open(url)
    }
}
